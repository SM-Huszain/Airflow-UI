# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.sensors.external_task import ExternalTaskSensor
# from airflow.utils import session
# from airflow.utils.dates import days_ago
# from airflow.operators.bash import BashOperator
# from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
# from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
# from airflow.sensors.filesystem import FileSensor
# from datetime import datetime, timedelta
# from airflow.models import DagRun,TaskInstance, dag
# from airflow.utils.session import provide_session
# from airflow.utils.state import State
# import airflow.settings
# from airflow.models import DagModel
# from airflow.models import TaskInstance
# from airflow.utils.session import provide_session
# import os

# AIRBYTE_CONNECTION_ID1 = 'd288718c-931d-4f4f-907e-00dbe856d3b7'
# AIRBYTE_CONNECTION_ID2 = 'a524ac08-580f-48d7-ac24-3bfa77f900a3'
# AIRBYTE_CONNECTION_ID3 = 'e139cafc-d246-47b4-8164-c70724694113'
       
# default_args = {
#     'owner': 'airflow',
# }

# with DAG(dag_id='ab_dag',
#          tags=['testing'],
#         default_args=default_args,
#         description='A DAG that runs every hour and skips the next run if the previous one failed',
#         schedule_interval='@once',
#         catchup=False,
#         max_active_runs=1,
#         start_date=days_ago(1)
#    ) as dag:
     
#      file_to_mysql = AirbyteTriggerSyncOperator(
#        task_id='file_to_mysql',
#        airbyte_conn_id='airbyte-connection',
#        connection_id=AIRBYTE_CONNECTION_ID1,
#        asynchronous=True,
#      )
     
#      file_to_mysql_sensor = AirbyteJobSensor(
#        task_id='file_to_mysql_sensor', 
#        airbyte_conn_id='airbyte-connection',
#        airbyte_job_id=file_to_mysql.output
#    )
     
#      mysql_to_postgres = AirbyteTriggerSyncOperator(
#        task_id='mysql_to_postgres',
#        airbyte_conn_id='airbyte-connection',
#        connection_id=AIRBYTE_CONNECTION_ID2,
#        asynchronous=True
#    )
     
#      mysql_to_postgres_sensor = AirbyteJobSensor(
#        task_id='mysql_to_postgres_sensor',
#        airbyte_conn_id='airbyte-connection',
#        airbyte_job_id=mysql_to_postgres.output
#    )
     
#      postgres_to_file = AirbyteTriggerSyncOperator(
#        task_id='postgres_to_file',
#        airbyte_conn_id='airbyte-connection',
#        connection_id=AIRBYTE_CONNECTION_ID3,
#        asynchronous=True
#    )
     
#     #  file_to_mysql >> file_to_mysql_sensor >> mysql_to_postgres >> mysql_to_postgres_sensor >> postgres_to_file 