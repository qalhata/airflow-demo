from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import requests
import pandas as pd
import os

@dag(schedule_interval='@daily', start_date=datetime(2023, 1, 1), catchup=False, tags=['advanced', 'currency'])
def currency_pipeline_advanced():

    @task()
    def fetch_data():
        url = 'https://open.er-api.com/v6/latest'
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame.from_dict(data['rates'], orient='index', columns=['rate'])
        df['currency'] = df.index
        df.reset_index(drop=True, inplace=True)
        df['timestamp'] = datetime.now().isoformat()
        df.to_csv('/opt/airflow/data/output.csv', index=False)
        return df.to_dict(orient='records')

    @task()
    def create_table_if_not_exists():
        pg_hook = PostgresHook(postgres_conn_id='pg_conn')
        create_sql = """
        CREATE TABLE IF NOT EXISTS exchange_rates(
            currency TEXT,
            rate NUMERIC,
            timestamp TIMESTAMP
        );
        """
        pg_hook.run(create_sql)

    @task()
    def load_to_postgres(records):
        pg_hook = PostgresHook(postgres_conn_id='pg_conn')
        insert_sql = """
            INSERT INTO exchange_rates (currency, rate, timestamp)
            VALUES (%(currency)s, %(rate)s, %(timestamp)s);
        """
        for row in records:
            pg_hook.run(insert_sql, parameters=row)

    # ✅ Correct chaining with variable assignment
    records = fetch_data()
    create = create_table_if_not_exists()
    create >> load_to_postgres(records)

currency_pipeline_advanced()
