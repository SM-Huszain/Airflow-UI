from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor


with DAG(
    dag_id='qualiz-poc',
    schedule="@once",
    start_date=days_ago(1),
    
    catchup=False,
) as dag:
   
    

    

    
    task1 = AirbyteTriggerSyncOperator(
        task_id='task1',
        airbyte_conn_id='airbyte-conn',
        connection_id='9c3a4aa5-d8ec-4b99-9336-000f34e6b280',
    )

    task1_sensor = AirbyteJobSensor(
        task_id='task1_sensor',
        airbyte_conn_id='airbyte-conn',
        airbyte_job_id=task1.output,
    )
    
    
    

    

    
    task2 = AirbyteTriggerSyncOperator(
        task_id='task2',
        airbyte_conn_id='airbyte-conn',
        connection_id='2013ed1e-cb4c-443e-a2d8-a068e92970a4',
    )

    task2_sensor = AirbyteJobSensor(
        task_id='task2_sensor',
        airbyte_conn_id='airbyte-conn',
        airbyte_job_id=task2.output,
    )
    
    
    

    
    
    task1 >> task1_sensor >> task2 >> task2_sensor