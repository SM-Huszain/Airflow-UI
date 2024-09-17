from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader('.'))
based_string = environment.get_template("sample.jinja")

dag_conf = {
    'dag_id' : 'dbt_jinja_dag',
    'tags' : ['testing'],
    'schedule_interval' : '@once',
    'catchup' : False,
    'max_active_runs' : 1,
    'start_date' : 'days_ago(1)',
    'dbt_types' : {
        'dbt_debug':{
             'bash_command':f"dbt debug --profiles-dir ~/.dbt --project-dir /mnt/d/dbt-project/dbt_project"
        },
        'dbt_seed':{
             'bash_command':f"dbt seed --profiles-dir ~/.dbt --project-dir /mnt/d/dbt-project/dbt_project"
        },
        'dbt_test':{
             'bash_command':f"dbt test --profiles-dir ~/.dbt --project-dir /mnt/d/dbt-project/dbt_project"
        },
        'dbt_run':{
             'bash_command':f"dbt run --profiles-dir ~/.dbt --project-dir /mnt/d/dbt-project/dbt_project"
        }
    }
}

with open('/home/hussain/airflow/dags/dbt_jinja_dag.py', 'w') as f :
    f.write(based_string.render(dag_conf))
    