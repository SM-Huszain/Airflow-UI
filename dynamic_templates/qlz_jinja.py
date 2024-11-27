
import os
from jinja2 import Environment, FileSystemLoader
from dynamic_templates.utils import get_cron

# template_dir = os.path.dirname(os.path.abspath(__file__),)
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))



environment = Environment(loader=FileSystemLoader(template_dir))
dag_template = environment.get_template("qlz.jinja")

def test(dag_conf):
    print(template_dir)
    dag_conf["schedule"]["repeat"] = get_cron(dag_conf["schedule"]["repeat"])
    
    with open("/mnt/d/airflow/dags/qlz_dag.py", "w") as f :
        f.write(dag_template.render(dag_conf=dag_conf))
    
    print("Changes Updated")


