import os
import sys
import mlflow
import dagshub
from urllib.parse import urlparse
import sklearn
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logging.logger import logging
from Networksecurity.entity.artifacts_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from Networksecurity.entity.config_entity import ModelTrainerConfig

from Networksecurity.utils.ml_utils.models.estimator import NetworkModel
from Networksecurity.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models,
)
from Networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import mlflow
import os
import tempfile
import joblib
# DagsHub MLflow tracking setup

import dagshub
dagshub.init(repo_owner='AlhassanAbubakarjnr',
             repo_name='NetworkSecurity_Ml_Project',
             mlflow=True)

os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/AlhassanAbubakarjnr/NetworkSecurity_Ml_Project.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "AlhassanAbubakarjnr"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "c86dc369c49644ea21e39abb3a14cfe61475990f"

# Model Trainer Class
class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def track_mlflow(self, best_model, classification_metric):
        """Log metrics and model safely to DagsHub MLflow."""
        with mlflow.start_run():
            mlflow.log_metric("f1_score", classification_metric.f1_score)
            mlflow.log_metric("recall_score", classification_metric.recall_score)
            mlflow.log_metric("precision_score", classification_metric.precision_score)

            #  Save and log model manually (DagsHub-safe)
            with tempfile.TemporaryDirectory() as tmp_dir:
                model_path = os.path.join(tmp_dir, "model.pkl")
                joblib.dump(best_model, model_path)
                mlflow.log_artifact(model_path, artifact_path="model")

    def train_model(self, x_train, y_train, x_test, y_test):
        """Train models, evaluate and log best one to MLflow"""
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }

        params = {
            "Decision Tree": {'criterion': ['gini', 'entropy', 'log_loss']},
            "Random Forest": {'n_estimators': [8, 16, 32, 128, 256]},
            "Gradient Boosting": {
                'learning_rate': [.1, .01, .05, .001],
                'subsample': [0.6, 0.7, 0.75, 0.85, 0.9],
                'n_estimators': [8, 16, 32, 64, 128, 256],
            },
            "Logistic Regression": {},
            "AdaBoost": {
                'learning_rate': [.1, .01, .001],
                'n_estimators': [8, 16, 32, 64, 128, 256],
            },
        }

        model_report = evaluate_models(
            X_train=x_train, y_train=y_train,
            X_test=x_test, y_test=y_test,
            models=models,param=params
        )

        # Get best model
        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model = models[best_model_name]

        # Train metrics
        y_train_pred = best_model.predict(x_train)
        classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
        self.track_mlflow(best_model, classification_train_metric)

        # Test metrics
        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
        self.track_mlflow(best_model, classification_test_metric)

        # Save the trained model
        preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
        model_file_path = os.path.dirname(self.model_trainer_config.model_trained_file_path)
        os.makedirs(model_file_path, exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.model_trained_file_path, obj=Network_Model)
        save_object("final_model/model.pkl", best_model)

        # Create artifact
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.model_trained_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """Load data, train models, and return artifact"""
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            X_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact = self.train_model(X_train, y_train, x_test, y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
