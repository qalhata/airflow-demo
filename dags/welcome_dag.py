from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests


def print_welcome():
    print('Welcome to ELM Airflow!')


def print_date():
    print('Today is {}'.format(datetime.today().date()))

def print_random_quote():
    try:
        response = requests.get('https://api.quotable.io/random')
        response.raise_for_status()
        quote = response.json().get('content', 'No quote found')
        print('Quote of the day: "{}"'.format(quote))
    except Exception as e:
        print(f"Failed to fetch quote: {e}")


# Define the DAG and its tasks
dag = DAG(
    'welcome_dag',
    default_args={'start_date': datetime.now() - timedelta(days=1)},
    schedule='0 23 * * *',
    catchup=False

)

print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=dag

)


print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag

)


print_random_quote = PythonOperator(

    task_id='print_random_quote',
    python_callable=print_random_quote,
    dag=dag

)


# Set the dependencies between the tasks

print_welcome_task >> print_date_task >> print_random_quote
