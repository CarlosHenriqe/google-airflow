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
    'retry_delay': timedelta(minutes=5)
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

def test():
    print('deu certo')
    return 

def save_df_to_gcs():
    df = extract_from_api()
    csv_data = df.to_csv(index=False)
    gcs_hook = GoogleCloudStorageHook(google_cloud_storage_conn_id='google_cloud_datastore_default')
    gcs_hook.upload(
        bucket='spotify-tables/podcasts-table-5',
        object='df.csv',
        data=csv_data.encode('utf-8'),
        mime_type='text/csv'
    )

dag = DAG(
    dag_id = 'write_table_5', 
    default_args=default_args, 
    schedule_interval='@hourly',
    start_date= datetime(2023,1,1),
    catchup = False,
    max_active_runs = 1,
    tags = ['spotify', 'source']
)

    # Tarefa para salvar o DataFrame diretamente no Google Cloud Storage
extract_task = PythonOperator(
    task_id='exctract',
    python_callable=save_df_to_gcs,
    dag = dag
)

load_task = PythonOperator(
    task_id='exctract',
    python_callable=test,
    dag = dag
)

extract_task >> load_task
globals()[dag.dag_id] = dag