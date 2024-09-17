from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader('.'))
based_string = environment.get_template("base.jinja")

dag_conf = {
    'dag_id' : 'jinja_dag',
    'tags' : ['testing'],
    'schedule_interval' : '@once',
    'catchup' : False,
    'max_active_runs' : 1,
    'start_date' : 'days_ago(1)',
    'connection' : 'airbyte-connection',   #connection in airflow
    'airbyte_connections' : {
        'file_to_mysql' :{
            'connection_id' : 'db7ff3eb-99d7-4f00-bccb-f12e60f1bf0e',
            'asynchronous' :   True  #true/false
        },
        'mysql_to_postgres' : {
            'connection_id' : '6445d121-b81d-4338-b8c0-16f5b34aa425',
            'asynchronous' :  True #true/false
        },
        'postgres_to_file' : {
            'connection_id' : '65c0179d-ae71-4fec-94f6-da8f87dc83e9',
            'asynchronous' : True  #true/false
        }
    }
}

with open('/home/hussain/airflow/dags/jinja_dag.py', 'w') as f :
    f.write(based_string.render(dag_conf))