FROM python:3.10-slim-bullseye

WORKDIR /app
COPY . .

# Install dependencies
RUN apt-get update -y && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["python", "app.py"]
