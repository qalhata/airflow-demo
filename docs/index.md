# 💡 Airflow Demo Labs: Data Engineering at Enterprise Scale

Welcome to the documentation for the **Airflow Demo Labs**. 
This site is automatically built using GitHub Pages and reflects all available labs in this repository.

---

## 🧪 Lab Modules Overview

### 1️⃣ Lab 1: Exchange Rate Pipeline
- 🔄 DAG Creation
- 📈 CSV Transformation
- 📤 Manual Testing Logic

📁 Location: `/lab1_airflow_exchange_rate/`

---

### 2️⃣ Lab 2: PostgreSQL Integration
- 📊 PostgreSQL Data Sink
- 🧮 Auto Table Creation
- 🧪 ETL Load Verification

📁 Location: `/lab2_PostgreSQL_Integration/`

---

### 3️⃣ Lab 3: NLP API Streaming
- 🤖 Sentiment Classification
- 📡 Streaming to Flask & FastAPI
- 🗃️ AI-Augmented Storage in PostgreSQL

📁 Location: `/lab3_NLP_API_streaming/`

---

## 🛠️ Technologies
- Apache Airflow 2.x+
- Docker & Compose
- PostgreSQL + pgAdmin
- Flask & FastAPI (NLP APIs)
- Python 3.10+

---

## How to Run Locally

```bash
# Clone the repo
git clone https://github.com/qalhata/airflow-demo.git
cd airflow-demo

# Build and run Lab 1
docker compose -f common/docker-compose.base.yml -f lab1_airflow_exchange_rate/docker-compose.lab1.yml up --build

# Replace 'lab1' with 'lab2' or 'lab3' as needed
```

## 🚀 Essential Resources(Reading Material)
[text](https://airflow.apache.org/docs/)
[text](https://docs.docker.com/compose/)
[text](https://fastapi.tiangolo.com/)