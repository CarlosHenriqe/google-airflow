from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'create_and_update_tables',
    default_args=default_args,
    description='DAG to create and update tables in BigQuery',
    schedule_interval=timedelta(minutes=30),  # Executar a cada 30 minutos
)

# Define the SQL query to create the derived table
create_table_sql = """
WITH BASE_2017 AS (
    SELECT DISTINCT 
        EXTRACT(YEAR FROM DATA_VENDA) || "-" || EXTRACT(MONTH FROM DATA_VENDA) AS ANO_MES,
        SUM(QTD_VENDA) AS QTD_VENDAS
    FROM `tabelas_boticario.base_2017`
    GROUP BY EXTRACT(YEAR FROM DATA_VENDA) || "-" || EXTRACT(MONTH FROM DATA_VENDA)
),
BASE_2019 AS (
    SELECT DISTINCT 
        EXTRACT(YEAR FROM DATA_VENDA) || "-" || EXTRACT(MONTH FROM DATA_VENDA) AS ANO_MES,
        SUM(QTD_VENDA) AS QTD_VENDAS
    FROM `tabelas_boticario.base_2019`
    GROUP BY EXTRACT(YEAR FROM DATA_VENDA) || "-" || EXTRACT(MONTH FROM DATA_VENDA)
)
SELECT 
    ANO_MES,
    QTD_VENDAS
FROM BASE_2017 
UNION ALL 
SELECT 
    ANO_MES,
    QTD_VENDAS
FROM BASE_2019
"""

# Create the derived table using the BigQueryExecuteQueryOperator
create_table = BigQueryExecuteQueryOperator(
    task_id='create_derived_table',
    sql=create_table_sql,
    use_legacy_sql=False,
    destination_dataset_table='default-case.bd_boticario.consolidado_ano_mes', # Replace with your destination table
    write_disposition='WRITE_TRUNCATE',
    dag=dag,
)

# Define the dependencies between the tasks
create_table
