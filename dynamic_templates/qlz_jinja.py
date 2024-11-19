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
        "repeat": "daily"
    },
    "tasks": [
        {
            "name": "task1",
            "description": "Extract data from api dump into Amazon S3 bucket",
            "type": "airbyte",
            "connectionId": "mtyj6rju54u76icdjt7i867i4e5uedh5",
            "airbyteConnection": "airbyte-connection"
        },
        {
            "name": "task2",
            "description": "Extract data from api and dump into Amazon S3 bucket",
            "type": "airbyte",
            "connectionId": "ryj568u679i6u43y4uhr6i67iy8oikyw4",
            "airbyteConnection": "airbyte-connection"
        }
    ],
    "createdAt": "",
    "updatedAt": ""
}

dag_conf["schedule"]["repeat"] = get_cron(dag_conf["schedule"]["repeat"])

with open("/home/hussain/airflow/dags/qlz_dag.py", "w") as f :
    f.write(dag_template.render(dag_conf=dag_conf))

print("File Created")


