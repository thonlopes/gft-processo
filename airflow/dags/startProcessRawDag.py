import airflow
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 3, 7),
    'retries': 0,
    'retry_delay': timedelta(hours=5)
}
with airflow.DAG('CarregaDadosCovidRaw',
                 default_args=default_args,
                 schedule_interval='@daily') as dag:
    dag_thon = BashOperator(
        task_id='sparkCovidRaw',
        bash_command="python3 /covid-app/src/teste.py",
    )
