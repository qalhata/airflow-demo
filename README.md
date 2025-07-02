![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![Python](https://img.shields.io/badge/python-3.12+-yellow?logo=python)
![Airflow](https://img.shields.io/badge/apache%20airflow-2.9+-brightgreen?logo=apacheairflow)
![License](https://img.shields.io/github/license/qalhata/airflow-demo)
![Last Commit](https://img.shields.io/github/last-commit/qalhata/airflow-demo)
![Open Issues](https://img.shields.io/github/issues/qalhata/airflow-demo)
![Stars](https://img.shields.io/github/stars/qalhata/airflow-demo?style=social)
![Forks](https://img.shields.io/github/forks/qalhata/airflow-demo?style=social)


# 🧠 Data Engineering Lab Series  
*Enterprise-Scale Pipelines with Airflow, PostgreSQL & AI APIs*

> **2025 Edition** | Modular Docker Labs | AI Integration | Async Streaming

---

## 📌 Table of Contents

- [🚀 Overview](#-overview)
- [🧰 Technologies Used](#-technologies-used)
- [📁 Folder Structure](#-folder-structure)
- [🔧 How to Run Each Lab](#-how-to-run-each-lab)
- [💡 Learning Keywords](#-learning-keywords)
- [🛠️ Suggested Extensions](#️-suggested-extensions)
- [📘 Final Notes](#-final-notes)


---

## 🚀 Overview

Welcome to a qtech selection **Data Engineering Labs**, built for practical training in modern enterprise-grade pipelines.  
This multi-lab setup simulates real-world engineering roles—complete with ETL orchestration, AI enrichment APIs, database integration, and async API comparisons.

| Lab | Description | Highlights |
|-----|-------------|------------|
| `Lab 1` | Exchange Rate ETL | Airflow DAGs, CSV exports |
| `Lab 2` | Postgres Integration | Database hooks, persistence |
| `Lab 3` | NLP API Streaming | Flask / FastAPI + DAG |  
| `Stretch` | FastAPI Async | Async vs Sync, OLTP vs OLAP |

---

## 🧰 Technologies Used

- 🧩 **Apache Airflow** — Orchestration engine for DAGs  
- 🐘 **PostgreSQL + pgAdmin** — Structured data storage and querying  
- 🔥 **Flask / FastAPI** — Lightweight APIs for AI enrichment  
- 🐳 **Docker Compose (modular)** — Environment automation

```bash
# Core Docker command to run any lab
docker compose -f common/docker-compose.base.yml -f labX/docker-compose.labX.yml up --build --force-recreate --no-cache

.
├── common/
│   └── docker-compose.base.yml          # Shared services
├── lab1_airflow_exchange_rate/
│   ├── dags/
│   └── docker-compose.lab1.yml
├── lab2_PostgreSQL_Integration/
│   ├── dags/
│   └── docker-compose.lab2.yml
├── lab3_NLP_API_streaming/
│   ├── dags/
│   ├── data/
│   ├── tweets.csv
│   ├── nlp_flask_api.py
│   ├── docker-compose.lab3.yml
└── README.md

## How to run each Lab

🔹 Step 1: Build & Start the Stack

# LAB 1: Airflow fetch pipeline
docker compose -f common/docker-compose.base.yml -f lab1_airflow_exchange_rate/docker-compose.lab1.yml up --build --force-recreate --no-cache

# LAB 2: PostgreSQL DAGs
docker compose -f common/docker-compose.base.yml -f lab2_PostgreSQL_Integration/docker-compose.lab2.yml up --build --force-recreate --no-cache

# LAB 3: NLP API + AI Streaming
docker compose -f common/docker-compose.base.yml -f lab3_NLP_API_streaming/docker-compose.lab3.yml up --build --force-recreate --no-cache

##🔹 Step 2: Access UIs

    🧠 Airflow → http://localhost:8080
    Login: airflow / airflow

    🐘 pgAdmin → http://localhost:5050
    Login: admin@admin.com / admin
    Server host: postgres, DB: airflow


##💡 Learning Keywords

    | Area          | Keywords                                              |
| ------------- | ----------------------------------------------------- |
| Orchestration | DAGs, scheduling, retries, decorators                 |
| Databases     | PostgreSQL, SQL hooks, pgAdmin                        |
| APIs          | Flask, FastAPI, REST, JSON                            |
| Architecture  | ETL/ELT, OLTP vs OLAP                                 |
| DevOps        | Docker Compose, modular environments                  |
| Advanced      | Concurrency, parallelism, async, enrichment pipelines |

## 🛠️ Suggested Extensions

    ✅ Add Great Expectations for validation

    📊 Add DBT for transformation modeling

    🚨 Add Slack/email alerts to DAGs

    🚀 Add Kafka/Redis for true streaming

    🧪 Benchmark FastAPI vs Flask under load


## 📘 Final Notes

    All DAGs are located under dags/

    Logs are stored in /opt/airflow/logs/

    Data files live under data/

    PostgreSQL tables must be created before running dependent tasks