from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

from bronze import ResidentEvil_to_BronzeMinio
from silver import ResidentEvil_Bronze_to_Silver
from gold import ResidentEvil_Silver_to_Gold

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'dag_resident_evil',
    default_args=default_args,
    description='Data Resildent Evil - data lake',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['resident_evil'],
) as dag:
    with TaskGroup(group_id='resident_evil_ingestion') as resident_evil_ingestion:
        pass