# Imports
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from clean_data import clean_data # Assuming clean_data.py is directly in the plugins folder

# Define or Instantiate DAG
dag = DAG(
    'exchange_rate_etl',
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    start_date=datetime(2023, 10, 1),
    end_date=datetime(2023, 12, 31),
    schedule='0 22 * * *',
    catchup=False
)

# Define or Instantiate Tasks
download_task = BashOperator(
    task_id='download_file',
    bash_command='curl -o xrate.csv https://www.floatrates.com/daily/usd.json',
    cwd='/tmp',
    dag=dag,
)

clean_data_task = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    dag=dag,
)

send_email_task = EmailOperator(
    task_id='send_email',
    to="{{ var.value.get('support_email', 'default-support@example.com') }}", # Use the support_email variable with a fallback
    subject='Exchange Rate Download - Successful',
    html_content='The Exchange Rate data has been successfully downloaded, cleaned, and loaded.',
    dag=dag,
)

# Define Task Dependencies
download_task >> clean_data_task >> send_email_task