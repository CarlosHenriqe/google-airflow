from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'update_consolidado_marca_ano_mes',
    default_args=default_args,
    description='DAG to create and update consolidated table in BigQuery',
    catchup=False,
    schedule_interval=timedelta(minutes=30),  # Executar a cada 30 minutos
)

# Define the SQL query to create/update the consolidated table
sql_query = """
WITH BASE_2017 AS (
  SELECT DISTINCT 
    MARCA,
    EXTRACT(YEAR FROM DATA_VENDA) AS ANO,
    EXTRACT(MONTH FROM DATA_VENDA) AS MES,
    SUM(QTD_VENDA) AS QTD_VENDAS
  FROM `default-case.bd_boticario.base_2017`
  GROUP BY
    MARCA,
    EXTRACT(YEAR FROM DATA_VENDA),
    EXTRACT(MONTH FROM DATA_VENDA)
),
BASE_2019 AS (
  SELECT DISTINCT 
    MARCA,
    EXTRACT(YEAR FROM DATA_VENDA) AS ANO,
    EXTRACT(MONTH FROM DATA_VENDA) AS MES,
    SUM(QTD_VENDA) AS QTD_VENDAS
  FROM `default-case.bd_boticario.base_2019`
  GROUP BY
    MARCA,
    EXTRACT(YEAR FROM DATA_VENDA),
    EXTRACT(MONTH FROM DATA_VENDA)
)
SELECT 
  ANO,
  MES,
  MARCA,
  QTD_VENDAS
FROM BASE_2017 
UNION ALL 
SELECT 
  ANO,
  MES,
  MARCA,
  QTD_VENDAS
FROM BASE_2019
"""

# Create/Update the consolidated table using the BigQueryExecuteQueryOperator
update_table = BigQueryExecuteQueryOperator(
    task_id='update_consolidado_marca_ano_mes',
    sql=sql_query,
    use_legacy_sql=False,
    destination_dataset_table='default-case.bd_boticario.consolidado_marca_ano_mes', # Replace with your destination table
    write_disposition='WRITE_TRUNCATE',  # Use 'WRITE_TRUNCATE' to update the table
    dag=dag,
)

# Define the dependencies between the tasks
update_table
