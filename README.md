# 🧠 Network Security Machine Learning Project

> 🚀 An end-to-end **MLOps pipeline** for real-time Network Intrusion Detection — from **data ingestion to cloud deployment** on **Azure App Service**.

---

## 📌 Overview

This project implements a **production-ready MLOps workflow** for detecting network anomalies (benign vs. malicious).  
It covers every phase of a modern ML lifecycle — **data collection**, **training**, **tracking**, **deployment**, and **continuous delivery**.

### 🎯 Objectives
- Build a robust ML pipeline for network threat classification.
- Automate training, versioning, and deployment using **MLflow** + **DagsHub**.
- Ensure reproducibility through **Docker** and **GitHub Actions**.
- Deploy seamlessly to **Azure Web App**.

---

## 🧩 Architecture

### 🏗️ MLOps Pipeline Overview
---

## 🧩 Architecture

### 🧠 MLOps Pipeline Architecture

![MLOps Architecture](https://github.com/AlhassanAbubakarjnr/NetworkSecurity_Ml_Project/raw/main/docs/mlops_architecture.jpg)


> *The architecture illustrates the complete end-to-end MLOps workflow — from data ingestion in MongoDB, model training & tracking with MLflow/DagsHub, to automated CI/CD deployment on Azure Web App.*

---


**Pipeline Flow:**

1. **Data Source (MongoDB)** — Stores raw network activity logs.
2. **Data Ingestion Layer** — Extracts and stores local datasets.
3. **Data Transformation Layer** — Handles preprocessing & feature engineering.
4. **Model Training & Tracking** — Managed via **MLflow** + **DagsHub**.
5. **Model Registry** — Keeps track of versioned models.
6. **FastAPI Serving (Dockerized)** — RESTful prediction endpoint.
7. **CI/CD (GitHub Actions)** — Automates testing, building, and deployment.
8. **Azure Web App** — Hosts the containerized model in production.

---

## 🗂️ Project Structure

```text
NetworkSecurity_Ml_Project/
│
├── .github/
│   └── workflows/                     # ⚙️ CI/CD pipelines
│       └── main_networksecurity.yml    # Azure deployment workflow
│
├── Networksecurity/                   # 🧠 Core ML pipeline package
│   ├── components/                    # Data ingestion, transformation, training scripts
│   ├── pipeline/                      # End-to-end pipeline orchestration
│   ├── utils/                         # Utility functions and helpers
│   ├── config/                        # Configuration files
│   └── __init__.py                    # Package initializer
│
├── final_model/                       # 🎯 Serialized models and preprocessors
│   ├── model.pkl                      # Trained ML model
│   └── preprocessor.pkl               # Feature transformer
│
├── Artifacts/                         # 📦 Auto-generated files (datasets, reports, etc.)
│
├── Dockerfile                         # 🐳 Docker image definition
├── requirements.txt                   # 📋 Python dependencies
├── app.py                             # 🚀 FastAPI app entrypoint for prediction
├── README.md                          # 🧾 Project documentation
└── setup.py                           # ⚙️ Package setup configuration

```
## 🧪 Local Development Setup (Windows)

### 🔹 Prerequisites

Before running the project locally, ensure you have the following installed:

- 🐍 **Python** ≥ 3.10  
- 🐳 **Docker Desktop**  
- 🌐 **MongoDB** (Atlas or Local instance)  
- ⚙️ **Git**  
- ☁️ **Azure Account** (for deployment)

---

### 🔹 Setup Steps (Windows)

---

### 🔹 Setup Steps

#### 1️⃣ Clone the Repository  
Clone the project to your local system using Git:

```bash
git clone https://github.com/AlhassanAbubakarjnr/NetworkSecurity_Ml_Project.git
cd NetworkSecurity_Ml_Project

```
2️⃣ Create a Virtual Environment

Create an isolated Python environment for the project:

```bash
python -m venv venv

```
3️⃣ Activate the Virtual Environment

Activate the environment in Windows PowerShell or CMD:

```bash
venv\Scripts\activate

```
4️⃣ Install Project Dependencies

Install all required Python libraries listed in requirements.txt:

```bash
pip install -r requirements.txt

```
5️⃣ Run the Application Locally

Start the FastAPI (or Flask) server:

```bash
python app.py

```
🐳 Run with Docker (Optional)

If you prefer running inside a Docker container:

Build the Docker Image
```bash
docker build -t networksecurity-ml .
```
Run the Container
```bash
docker run -d -p 8000:8000 networksecurity-ml

```
# 🧰 Troubleshooting Guide (Windows)

This guide provides quick solutions to common issues encountered during setup, development, or deployment of your **Network Security ML Project**.  
Each issue includes the cause, explanation, and copy-ready fixes.

---

## ⚙️ 1️⃣ Virtual Environment Activation Error

If PowerShell blocks activation with an error like:
~~~bash
venv\Scripts\activate : cannot be loaded because running scripts is disabled on this system.
~~~

✅ **Fix: Enable script execution**
~~~bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
~~~

---

## 📦 2️⃣ Dependency Installation Fails

If you encounter missing packages or pip errors, upgrade pip and reinstall:
~~~bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
~~~

If a specific package fails, install it manually:
~~~bash
pip install <package-name>
~~~

---

## 🌐 3️⃣ MongoDB Connection Error

If your app fails to connect to MongoDB, verify that MongoDB is running or your Atlas connection string is correct.

Example connection URI:
~~~bash
mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
~~~

✅ Replace `<username>` and `<password>` with valid credentials.  
✅ Ensure network access in MongoDB Atlas allows your current IP address.

---

## 🧱 4️⃣ Port Already in Use

If you see:
~~~bash
OSError: [Errno 98] Address already in use
~~~

✅ **Fix: Free the port**
~~~bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
python app.py
~~~

Replace `<PID>` with the process ID from the netstat command.

---

## 🐳 5️⃣ Docker Build or Run Fails

Ensure **Docker Desktop** is running and you are in the **project root directory**.

### 🔹 Build image
~~~bash
docker build -t networksecurity-ml .
~~~

### 🔹 Run container
~~~bash
docker run -p 8000:8000 networksecurity-ml
~~~

If the build fails, clean up unused images and cache:
~~~bash
docker system prune -a
docker build -t networksecurity-ml .
~~~

---

## ☁️ 6️⃣ Azure Deployment Issues

If your **GitHub Action** fails to deploy to Azure:

✅ **Check these:**
- The **Azure Publish Profile secret** exists in  
  `Settings → Secrets and variables → Actions → AZUREAPPSERVICE_PUBLISHPROFILE_<ID>`
- Your YAML workflow file name matches `main_networksecurity.yml`
- The app name in the workflow matches your Azure Web App name

To redeploy manually:
~~~bash
git add .
git commit -m "Redeploying to Azure"
git push origin main
~~~

Then re-run the workflow from **GitHub → Actions tab**.

---

## 🧹 7️⃣ Reset Virtual Environment (Last Resort)

If dependency conflicts persist, reset your environment.

### 🔹 Delete and recreate the venv
~~~bash
rd /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
~~~

### 🔹 Sync current dependencies
~~~bash
pip freeze > requirements.txt
~~~

---

## 💡 Pro Tips

- Always activate the virtual environment before running scripts.  
- Commit only essential files — exclude `/venv`, `/__pycache__/`, and `.pkl` files.  
- Keep Docker and Azure CLI updated.  
- Regularly monitor the `requirements.txt` for version consistency.  
- Check GitHub Actions logs for detailed CI/CD errors.

---


---

## 🧱 GitHub Actions Workflow Summary

📄 **Workflow file:** `.github/workflows/main_networksecurity.yml`

The pipeline includes **two main jobs** — `build` and `deploy`:

1️⃣ **Build Phase**
- Checks out repository  
- Sets up Python (v3.10)  
- Installs dependencies  
- Packages the app as an artifact  

2️⃣ **Deploy Phase**
- Downloads the artifact  
- Uses the Azure publish profile secret  
- Deploys the web app automatically  

---

### ⚙️ Key Configuration Parameters

| Parameter | Description |
|------------|-------------|
| `app-name` | Your Azure Web App name (must match Azure portal) |
| `publish-profile` | GitHub Actions secret key for Azure deployment |
| `python-version` | Version for build environment |
| `slot-name` | Default: `Production` |
| `branches` | Pipeline triggers on `main` branch |

---

## 🧪 Local Setup for Testing Before CI/CD

Follow this to replicate CI/CD steps manually on your Windows environment.

### 🔹 Step 1: Clone Repository
~~~bash
git clone https://github.com/AlhassanAbubakarjnr/NetworkSecurity_Ml_Project.git
cd NetworkSecurity_Ml_Project
~~~

### 🔹 Step 2: Create and Activate Virtual Environment
~~~bash
python -m venv venv
venv\Scripts\activate
~~~

### 🔹 Step 3: Install Dependencies
~~~bash
pip install -r requirements.txt
~~~

### 🔹 Step 4: Run Application Locally
~~~bash
python app.py
~~~

Your API should be available at  
👉 **http://127.0.0.1:8000**

---

## 🧰 Troubleshooting Guide (Windows)

This section summarizes common problems you might encounter during development or deployment and their fixes.

---

### ⚙️ 1️⃣ Virtual Environment Activation Error
If you see:
~~~bash
venv\Scripts\activate : cannot be loaded because running scripts is disabled on this system.
~~~
✅ **Fix**
~~~bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
~~~

---

### 📦 2️⃣ Dependency Installation Fails
Upgrade pip and reinstall:
~~~bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
~~~

---

### 🌐 3️⃣ MongoDB Connection Error
Ensure correct credentials and IP access:
~~~bash
mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
~~~

---

### 🧱 4️⃣ Port Already in Use
Free the port and restart the app:
~~~bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
python app.py
~~~

---

### 🐳 5️⃣ Docker Build or Run Fails
Ensure Docker Desktop is running:
~~~bash
docker build -t networksecurity-ml .
docker run -p 8000:8000 networksecurity-ml
~~~
If errors persist:
~~~bash
docker system prune -a
docker build -t networksecurity-ml .
~~~

---

### ☁️ 6️⃣ Azure Deployment Issues
- Check the publish profile secret exists under:
  **Settings → Secrets and variables → Actions**
- Ensure workflow app name matches your Azure Web App

Redeploy manually:
~~~bash
git add .
git commit -m "Redeploying to Azure"
git push origin main
~~~

---

### 🧹 7️⃣ Reset Virtual Environment
~~~bash
rd /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
~~~

---

## 💡 Best Practices

- Activate `venv` before every run  
- Do **not** commit `venv/`, `__pycache__/`, or `.pkl` files  
- Keep Docker and Azure CLI up to date  
- Monitor GitHub Actions logs for any CI/CD failure  
- Use semantic commit messages (e.g., `fix:`, `feat:`, `chore:`)

---

## ✅ Summary

| Category | Description |
|-----------|--------------|
| **CI/CD Tool** | GitHub Actions |
| **Cloud Platform** | Azure App Service |
| **Containerization** | Docker |
| **App Framework** | FastAPI |
| **Data Source** | MongoDB |
| **Tracking** | MLflow + DagsHub |
| **Version Control** | Git & GitHub |
| **Environment** | Windows (Primary Dev OS) |

---
