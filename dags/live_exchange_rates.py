# Import
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta

# Define the DAG
dag = DAG(
    'live_exchange_rates',
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 21 * * *',
    catchup=False,

)

# Define the Tasks
fetch_exchange_rates = BashOperator(
    task_id='fetch_exchange_rates',
    # Ensure 'web_api_key' variable contains the full, correct URL or that the command is structured accordingly.
    bash_command="curl -fSsl '{{ var.value.get('web_api_key') }}' -o /tmp/xrate.json",
    cwd='/tmp',
    dag=dag,

)

send_email_task = EmailOperator(
    task_id='send_email',
    to="{{ var.value.get('support_email') }}",
    subject='Live Exchange Rate Download - Successful',
    # Consider adding dynamic content or attaching the file if useful
    html_content='Live Exchange Rate data has been successfully downloaded to /tmp/xrate.json on the worker.',
    dag=dag,

)

# Define the Dependencies

fetch_exchange_rates >> send_email_task