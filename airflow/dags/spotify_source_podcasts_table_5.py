from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from google.cloud import bigquery
import requests
import pandas as pd

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def extract_from_api():
    url = "https://spotify-api-tibfvjde4q-uc.a.run.app/podcasts"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Data obtained successfully:")
        # Create DataFrame from JSON
        df = pd.DataFrame(data)
        # Select only the desired columns
        selected_columns = ["name", "description", "id", "total_episodes"]
        df_selected = df[selected_columns]

        return df_selected
    else:
        print(f"Error making the request. Status code: {response.status_code}")

def save_df_to_gcs():
    df = extract_from_api()
    csv_data = df.to_csv(index=False)
    print("CSV data:")
    print(csv_data)
    gcs_hook = GCSHook(gcp_conn_id='google_cloud_datastore_default')
    gcs_hook.upload(
        bucket_name='spotify-tables',
        object_name='podcasts-table-5/df.csv',
        data=csv_data.encode('utf-8'),
        mime_type='text/csv'
    )
    print("Data uploaded to GCS successfully.")

def create_bigquery_table():

    project_id = 'default-case'
    dataset_id = 'bd_boticario'
    table_id = 'spotify_source_table_5'

    schema = [
        bigquery.SchemaField('name', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('description', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('id', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('total_episodes', 'INTEGER', mode='NULLABLE'),
    ]

    bucket_path = 'gs://spotify-tables/podcasts-table-5/df.csv'

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1
    )

    bq_client = bigquery.Client(project=project_id)
    bq_client.delete_table(f"{project_id}.{dataset_id}.{table_id}", not_found_ok=True)
    print("Table deleted successfully.")
    bq_client.create_table(bigquery.Table(f"{project_id}.{dataset_id}.{table_id}", schema=schema))
    print("Empty table created successfully.")
    job = bq_client.load_table_from_uri(bucket_path, f"{project_id}.{dataset_id}.{table_id}", job_config=job_config)
    job.result()  # Wait for the job to complete
    print("Data loaded into BigQuery table successfully.")

dag = DAG(
    dag_id='spotify_source_table_5',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['spotify', 'source']
)

# Task to save the DataFrame directly to Google Cloud Storage
extract_task = PythonOperator(
    task_id='extract',
    python_callable=save_df_to_gcs,
    dag=dag
)

load_task = PythonOperator(
    task_id='load',
    python_callable=create_bigquery_table,
    dag=dag
)

extract_task >> load_task
globals()[dag.dag_id] = dag
