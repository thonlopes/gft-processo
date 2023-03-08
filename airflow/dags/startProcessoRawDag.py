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
        'carrega-dados-covid',
        schedule_interval='@daily',
        default_args=default_args) as dag:
    
    carrega_raw = BashOperator(
        task_id='carrega-raw',
        bash_command="python3 /covid-app/src/startProcessoRaw.py",
    )
    
    carrega_trusted = BashOperator(
        task_id='carrega-trusted',
        bash_command="python3 /covid-app/src/startProcessoTrusted.py",
    )

    carrega_raw >> carrega_trusted