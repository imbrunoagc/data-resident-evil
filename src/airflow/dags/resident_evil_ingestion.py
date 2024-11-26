from datetime import timedelta, datetime

from airflow.decorators import dag, task
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.utils.dates import days_ago
# from airflow.utils.task_group import TaskGroup


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

@dag(
    dag_id="resident_evil",
    description="pipeline",
    schedule="* * * * *",
    start_date=datetime(2024, 11, 25),
    catchup=False
)
def pipeline_resident_evil():
    
    @task
    def extractor_data_and_ingestion_to_bronze():
        ResidentEvil_to_BronzeMinio().run_bronze(
            'resident-evil', 'bronze/person_characters.json'
        )
    
    @task
    def transform_data_from_bronze_to_silver():
        ResidentEvil_Bronze_to_Silver().bronze_to_silver()

    @task
    def silver_to_gold():
        ResidentEvil_Silver_to_Gold().generate_tables_gold()

    extractor_data_and_ingestion_to_bronze() >> transform_data_from_bronze_to_silver() >> silver_to_gold()

pipeline_resident_evil()