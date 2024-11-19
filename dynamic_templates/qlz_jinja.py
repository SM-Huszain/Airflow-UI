from jinja2 import Environment, FileSystemLoader
from utils import get_cron

environment = Environment(loader=FileSystemLoader("."))
dag_template = environment.get_template("qlz.jinja")

dag_conf = {
    "jobName": "Qualiz-POC",
    "description": "",
    "schedule": {
        "start": "days_ago(1)",
        "end": "",
        "repeat": "never"
    },
    "tasks": [
        {
            "name": "task1",
            "description": "Extract data from api dump into Amazon S3 bucket",
            "type": "airbyte",
            "connectionId": "d71a609d-a6f2-4b87-a32d-5022cffc2d75",
            "airbyteConnection": "airbyte-connection",
            'asynchronous' :  True
        },
        {
            "name": "task2",
            "description": "Extract data from api and dump into Amazon S3 bucket",
            "type": "airbyte",
            "connectionId": "fc5f9601-48c2-4708-ace5-b39b61f016be",
            "airbyteConnection": "airbyte-connection",
            'asynchronous' :  True
        }
    ],
    "createdAt": "",
    "updatedAt": ""
}

dag_conf["schedule"]["repeat"] = get_cron(dag_conf["schedule"]["repeat"])

with open("/home/hussain/airflow/dags/qlz_dag.py", "w") as f :
    f.write(dag_template.render(dag_conf=dag_conf))

print("Changes Updated")
