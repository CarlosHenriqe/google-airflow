from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from google.cloud import storage

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'update_sales_table_1',
    default_args=default_args,
    description='DAG to update Boticario tables in BigQuery',
    schedule_interval=timedelta(minutes=30),  # Executar a cada 30 minutos
)

# Função para ler o SQL do arquivo update_query.sql no bucket
def read_sql_from_file(bucket_name, file_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_path)
    sql_query = blob.download_as_text()
    return sql_query

bucket_name = 'us-east1-airflow-gcp-54adddd8-bucket/dags/sales_sqls'  # Substitua pelo nome real do seu bucket
file_path = 'us-east1-airflow-gcp-54adddd8-bucket/dags/sales_sqls/table_1.sql'  # Substitua pelo caminho real do arquivo no bucket
sql_query = read_sql_from_file(bucket_name, file_path)

update_bq_tables = BigQueryExecuteQueryOperator(
    task_id='update_bq_table_1',
    sql=sql_query,
    use_legacy_sql=False,
    dag=dag,
)

update_bq_tables
