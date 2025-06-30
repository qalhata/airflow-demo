from airflow.decorators import dag, task
from datetime import datetime
import pandas as pd
import requests
import os
import logging

@dag(
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['exchange'],
    default_args={'retries': 1}
)
def exchange_rate_pipeline():

    @task()
    def fetch_data():
        url = 'https://open.er-api.com/v6/latest'

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Full API Response: {data}")

            if 'rates' not in data:
                raise KeyError("Expected key 'rates' not found in API response: {}".format(data))

            df = pd.DataFrame.from_dict(data['rates'], orient='index', columns=['rate'])
            df['currency'] = df.index
            df.reset_index(drop=True, inplace=True)
            return df.to_dict()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise
        except Exception as e:
            logging.error(f"Error in fetch_data: {e}")
            raise

    @task()
    def transform_data(data_dict):
        try:
            df = pd.DataFrame.from_dict(data_dict)
            df['rate'] = df['rate'].astype(float)
            df.sort_values(by='rate', ascending=False, inplace=True)
            return df.to_csv(index=False)
        except Exception as e:
            logging.error(f"Error in transform_data: {e}")
            raise

    @task()
    def save_to_file(csv_data):
        output_path = '/opt/airflow/files/exchange_rates.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(csv_data)
        logging.info(f"Saved data to {output_path}")

    save_to_file(transform_data(fetch_data()))

exchange_rate_pipeline()