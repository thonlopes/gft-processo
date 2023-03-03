import airflow
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 2, 5),
    'retries': 0,
    'retry_delay': timedelta(hours=5)
}
with airflow.DAG('dag_thon',
                 default_args=default_args,
                 schedule_interval='@daily') as dag:
    dag_thon = BashOperator(
        task_id='teste_thon_spark',
        bash_command="python /covid-app/src/processa_covid_raw.py",
    )
