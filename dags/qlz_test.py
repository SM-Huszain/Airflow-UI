import sys
import os
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.bash import BashOperator
sys.path.append(os.path.abspath("/mnt/d/airflow"))
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from dynamic_templates.qlz_jinja import test
from datetime import timedelta


def connect_db():
    pass 

    import psycopg2
    
    try:
        conn = psycopg2.connect(
            dbname="ab_psql",
            user="postgres", 
            password="password",
            host="localhost",  
            port=5432,
        )
        print("Connected successfully!")

        cursor = conn.cursor() 
        select_table = "SELECT * FROM job_config"
        cursor.execute(select_table)
        records = cursor.fetchall()
        print(records[0][1])
        test(records[0][1])

    except Exception as e:
        print(f"Error: {e}")  


def get_dag():
    from airflow.models import DagBag
 
    dag_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    dagbag = DagBag(dag_folder=dag_folder)
    dag = dagbag.get_dag('qualiz-poc')
    
    print("################ {dag} ################")
    print(dag.dag_id)  
    return dag.dag_id



with DAG( 
    dag_id='qlz_fetch_conn',
    default_args={'execution_timeout': timedelta(minutes=60)}, 
    tags=['qlz-testing'],
    schedule="@once",
    catchup=False, 
    max_active_runs=1,  
    start_date=days_ago(1),
) as dag: 

    fetch_config = PythonOperator(
        task_id="fetch_config", 
        python_callable=connect_db
    )

    fetch_dag = PythonOperator(
        task_id="fetch_dag", 
        python_callable=get_dag,
        execution_timeout=timedelta(minutes=30),
    )

    # task2 = BashOperator(
    #     task_id='task2',
    #     bash_command='echo "{{ ti.xcom_pull(task_ids=\'fetch_dag\') }}"',
    # )

    def get_trigger_dag_id(context):
        ti = context['ti']
        return ti.xcom_pull(task_ids='fetch_dag')

    trigger_other_dag = TriggerDagRunOperator(
        task_id="trigger_another_dag", 
        trigger_dag_id="qualiz-poc", 
        wait_for_completion=True, 
    )

    
    fetch_config >> fetch_dag >> trigger_other_dag

