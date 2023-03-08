import airflow
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 3, 7),
    'retries': 0,
    'retry_delay': timedelta(hours=5)
}

with airflow.DAG(
        'carrega-dados-covid-refined',
        schedule_interval='@daily',
        default_args=default_args) as dag:
    
    carrega_refined = BashOperator(
        task_id='carrega-refined',
        bash_command="python3 /covid-app/src/startProcessoRefined.py",
    )
