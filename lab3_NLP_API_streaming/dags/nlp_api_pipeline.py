from airflow.decorators import dag, task
from datetime import datetime
import pandas as pd
import requests
from airflow.providers.postgres.hooks.postgres import PostgresHook

@dag(schedule_interval='@daily', start_date=datetime(2023, 1, 1), catchup=False, tags=['nlp'])
def nlp_api_pipeline():

    @task()
    def load_data():
        df = pd.read_csv('/opt/airflow/data/tweets.csv')
        return df.to_dict(orient='records')

    @task()
    def enrich_sentiment(records):
        enriched = []
        for row in records:
            response = requests.post('http://nlp-api:5000/analyze', json={"text": row['text']})
            sentiment = response.json().get("sentiment")
            row['sentiment'] = sentiment
            enriched.append(row)
        return enriched

    @task()
    def create_table_if_not_exists():
        pg_hook = PostgresHook(postgres_conn_id='pg_conn')
        create_sql = """
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY,
                text TEXT,
                sentiment TEXT
            );
        """
        pg_hook.run(create_sql)

    
    @task()
    def store_pg(data):
        pg_hook = PostgresHook(postgres_conn_id='pg_conn')
        sql = """
            INSERT INTO tweets (id, text, sentiment)
            VALUES (%(id)s, %(text)s, %(sentiment)s);
        """
        for row in data:
            pg_hook.run(sql, parameters=row)

    store_pg(enrich_sentiment(load_data()))
    create_table_if_not_exists() >> load_data()

nlp_api_pipeline()
