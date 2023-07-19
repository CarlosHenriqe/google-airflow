from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
import requests
import pandas as pd

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 7, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_from_api():
    url = "https://spotify-api-tibfvjde4q-uc.a.run.app/podcasts"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Dados obtidos com sucesso:")
        # Criar DataFrame a partir do JSON
        df = pd.DataFrame(data)
        # Selecionar apenas os campos desejados
        selected_columns = ["name", "description", "id", "total_episodes"]
        df_selected = df[selected_columns]

        return df_selected
    else:
        print(f"Erro ao fazer a solicitação. Status code: {response.status_code}")

def save_df_to_gcs():
    df = extract_from_api()
    csv_data = df.to_csv(index=False)
    gcs_hook = GoogleCloudStorageHook(google_cloud_storage_conn_id='your_gcp_connection')
    gcs_hook.upload(
        bucket='spotify-tables/podcasts-table-5',
        object='df.csv',
        data=csv_data.encode('utf-8'),
        mime_type='text/csv'
    )

with DAG('write_df_to_csv', default_args=default_args, schedule_interval='@hourly') as dag:

    # Tarefa para salvar o DataFrame diretamente no Google Cloud Storage
    save_df_gcs = PythonOperator(
        task_id='save_df_gcs',
        python_callable=save_df_to_gcs
    )

    save_df_gcs