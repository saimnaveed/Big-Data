from airflow import DAG
from airflow.operators.python import PythonOperator
#from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.crypto_etl import main

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
    'start_date': datetime(2025, 7, 10)
}

with DAG('crypto_etl_v3', default_args=default_args, description="Generates a daily report",
  schedule_interval="35 14 * * *",  #setting time for dag execution
  catchup=False,                    # only run for current/future dates
  tags=["example"]
  ) as dag:
    
  extract_task = PythonOperator(
      task_id='fetch_binance_data',
      python_callable=main)
  extract_task
