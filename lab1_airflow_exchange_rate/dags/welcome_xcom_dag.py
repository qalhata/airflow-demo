from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import requests


def fetch_quote():
    try:
        response = requests.get('https://api.quotable.io/random')
        response.raise_for_status()
        quote = response.json().get('content', 'No quote found')
        print(f"Fetched quote: {quote}")
        return quote  # 👈 XCom value is returned here
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return "Default inspirational quote."


def display_quote(**context):
    # 👇 Pull the value using XComs
    quote = context['ti'].xcom_pull(task_ids='fetch_quote')
    print(f"Quote passed via XCom: '{quote}'")


def print_welcome():
    print('Welcome to ELM Airflow XCom demo!')


def print_date():
    from datetime import datetime
    print(f"Today is {datetime.today().date()}")


def print_separator():
    print("====================")

with DAG(
    dag_id='welcome_xcom_dag',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(1),
        'retries': 0
    },
    description='A demo DAG for showcasing XCom between tasks',
    schedule_interval=None,
    catchup=False,
    tags=['demo', 'xcom']
) as dag:

    welcome = PythonOperator(
        task_id='print_welcome',
        python_callable=print_welcome
    )

    date = PythonOperator(
        task_id='print_date',
        python_callable=print_date
    )

    separator = PythonOperator(
        task_id='print_separator',
        python_callable=print_separator
    )

    fetch = PythonOperator(
        task_id='fetch_quote',
        python_callable=fetch_quote
    )

    display = PythonOperator(
        task_id='display_quote',
        python_callable=display_quote,
        provide_context=True
    )

    # DAG Execution Order
    welcome >> date >> separator >> fetch >> display