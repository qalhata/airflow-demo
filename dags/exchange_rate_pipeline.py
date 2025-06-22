# Imports
from __future__ import annotations

from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.email import EmailOperator

from clean_data import clean_data  # Assuming clean_data.py is in the plugins folder


@dag(
    dag_id='exchange_rate_etl',
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    start_date=datetime(2023, 10, 1),
    end_date=datetime(2023, 12, 31),
    schedule='0 22 * * *',
    catchup=False,
    doc_md="""
    ### Exchange Rate ETL
    This DAG downloads daily exchange rate data, cleans it using a custom plugin,
    and sends a success notification. It demonstrates a modern ETL pattern using the TaskFlow API.
    """
)
def exchange_rate_etl_dag():
    """
    #### Exchange Rate ETL Pipeline
    Downloads, cleans, and stores exchange rate data.
    """
    INPUT_FILEPATH = '/tmp/xrate.json'
    OUTPUT_DIR = '/opt/airflow/data/xrate_cleansed'

    @task.bash
    def download_file() -> str:
        """Downloads the exchange rate JSON and returns the file path."""
        # The last line of a bash script is returned as the task's output (XCom)
        return f"curl -fSsl -o {INPUT_FILEPATH} https://www.floatrates.com/daily/usd.json && echo {INPUT_FILEPATH}"

    @task
    def clean_downloaded_data(input_path: str):
        """A TaskFlow wrapper around the clean_data function from the plugin."""
        clean_data(input_path=input_path, output_dir=OUTPUT_DIR)

    email_notification = EmailOperator(
        task_id='send_email',
        to="{{ var.value.get('support_email', 'default-support@example.com') }}",
        subject='Exchange Rate ETL for {{ ds }} - Successful',
        html_content="""
            <h3>ETL Process Complete</h3>
            <p>The Exchange Rate data for <b>{{ ds }}</b> has been successfully downloaded, cleaned, and loaded.</p>
        """,
    )

    # Define Task Dependencies using TaskFlow API
    input_filepath = download_file()
    cleaned_task = clean_downloaded_data(input_filepath)
    cleaned_task >> email_notification


exchange_rate_etl_dag()