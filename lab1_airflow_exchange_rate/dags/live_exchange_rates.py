# Import

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator

@dag(
    dag_id='live_exchange_rates',
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 21 * * *',
    catchup=False,
    doc_md="""
    ### Live Exchange Rates ETL

    This DAG downloads live exchange rate data, processes it, and sends a notification email.
    It demonstrates a simple ETL pattern using Bash, Python, and Email operators with the TaskFlow API.
    """
)
def live_exchange_rates_etl():
    """
    #### Live Exchange Rates ETL
    This DAG downloads live exchange rate data, processes it, and sends a notification email.
    """
    @task.bash
    def fetch_exchange_rates() -> str:
        """Downloads exchange rate data and returns the file path."""
        # This script now checks for the variable and provides a clear error if it's missing.
        return """
        API_URL="{{ var.value.get('web_api_key', 'MISSING') }}"
        API_KEY="{{ var.value.get('api_access_key', 'MISSING')}}"
        if [[ "$API_URL" == "MISSING" ]]; then
            echo "ERROR: Airflow Variable 'web_api_key' is not set. Please set it in the Airflow UI."
            exit 1
        fi
        curl -fSsl -H "apikey: $API_KEY" "$API_URL" -o /tmp/xrate.json && echo /tmp/xrate.json
        """

    @task
    def process_json_data(file_path: str) -> dict:
        """Reads the downloaded JSON file, logs key info, and returns it."""
        if not file_path or not isinstance(file_path, str):
            raise ValueError(f"Invalid file_path received: {file_path}. Upstream task may have failed to produce output.")

        clean_file_path = file_path.strip()
        logging.info(f"Processing file: '{clean_file_path}'")
        try:
            with open(clean_file_path, 'r') as f:
                data = json.load(f)
            
            if not data:
                raise ValueError("JSON file is empty or contains no data.")

            processed_info = {'base_currency': data.get('base'), 'rate_date': data.get('date')}
            logging.info(f"Successfully processed data: {processed_info}")
            return processed_info
        except FileNotFoundError:
            logging.error(f"File not found at path: '{clean_file_path}'")
            raise
        except json.JSONDecodeError:
            logging.error(f"Could not decode JSON from file: '{clean_file_path}'")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred while processing file '{clean_file_path}': {e}")
            raise

    def send_email_via_python_operator(**context):
        """
        Sends an email using smtplib.SMTP_SSL, fetching details from 'smtp_default' connection.
        This function replaces the EmailOperator for more direct control over SSL.
        """
        import smtplib
        import ssl
        from email.mime.text import MIMEText
        from airflow.hooks.base import BaseHook

        logging.info("Attempting to send email directly via PythonOperator.")
        try:
            conn = BaseHook.get_connection('smtp_default')
        except Exception as e:
            logging.error(f"Failed to get 'smtp_default' connection: {e}")
            raise

        # Extract connection details
        smtp_host = conn.host
        smtp_port = conn.port
        smtp_user = conn.login
        smtp_password = conn.password
        sender_email = conn.login
        
        # Get recipient email from Airflow Variable, with a fallback
        to_email = context['ti'].xcom_pull(task_ids=None, key='var.value.support_email')
        if not to_email:
            to_email = "devops@qalhatatech.com" # Fallback if variable not set
            logging.warning(f"Airflow Variable 'support_email' not found, using fallback: {to_email}")
        
        # Prepare email content (using XComs from processed_json_data task)
        processed_data = context['ti'].xcom_pull(task_ids='process_json_data')
        base_currency = processed_data.get('base_currency', 'N/A') if processed_data else 'N/A'
        rate_date = processed_data.get('rate_date', 'N/A') if processed_data else 'N/A'

        subject = f"Live Exchange Rate for {base_currency} - Successful"
        html_content = f"""
            <h3>Live Exchange Rate Download Successful</h3>
            <p>Data for base currency <b>{base_currency}</b>
            from <b>{rate_date}</b>
            has been successfully downloaded and processed.</p>
        """

        message = MIMEText(html_content, 'html')
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = to_email

        ssl_context = ssl.create_default_context()
        try:
            logging.info(f"Connecting to {smtp_host}:{smtp_port} with smtplib.SMTP_SSL...")
            with smtplib.SMTP_SSL(smtp_host, smtp_port, context=ssl_context) as server:
                logging.info("Connection successful.")
                server.login(smtp_user, smtp_password)
                logging.info("Login successful.")
                server.sendmail(sender_email, [to_email], message.as_string())
                logging.info(f"Email sent successfully to {to_email}!")
        except Exception as e:
            logging.error(f"Email sending FAILED: {e}")
            raise

    # The EmailOperator can directly consume the output of the upstream TaskFlow task
    # The `processed_data` variable holds the XCom from the `process_json_data` task
    file_path_output = fetch_exchange_rates()
    processed_data = process_json_data(file_path_output)

    # Use the custom PythonOperator for email sending
    send_final_email_task = PythonOperator(
        task_id='send_email', # Keep the same task_id for consistency
        python_callable=send_email_via_python_operator,
    )

    processed_data >> send_final_email_task

live_exchange_rates_etl()
