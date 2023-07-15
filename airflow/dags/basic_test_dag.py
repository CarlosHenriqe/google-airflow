from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# Define o nome da DAG e sua descrição
dag = DAG(
    'hello_world',
    description='Exemplo de DAG que executa uma tarefa "Olá Mundo"',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1)
)

# Define a tarefa "Olá Mundo" usando o operador BashOperator
hello_task = BashOperator(
    task_id='hello_task',
    bash_command='echo "Olá Mundo"',
    dag=dag
)

# Define a dependência entre as tarefas
hello_task
