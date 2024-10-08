#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Example Airflow DAG for Google AutoML service testing model operations."""

from __future__ import annotations

import os
from datetime import datetime

from google.protobuf.struct_pb2 import Value

from airflow.models.dag import DAG
from airflow.providers.google.cloud.operators.automl import (
    AutoMLBatchPredictOperator,
    AutoMLCreateDatasetOperator,
    AutoMLDeleteDatasetOperator,
    AutoMLDeleteModelOperator,
    AutoMLGetModelOperator,
    AutoMLImportDataOperator,
    AutoMLPredictOperator,
    AutoMLTrainModelOperator,
)
from airflow.providers.google.cloud.operators.gcs import (
    GCSCreateBucketOperator,
    GCSDeleteBucketOperator,
    GCSSynchronizeBucketsOperator,
)
from airflow.utils.trigger_rule import TriggerRule

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID", "default")
DAG_ID = "automl_model"
GCP_PROJECT_ID = os.environ.get("SYSTEM_TESTS_GCP_PROJECT", "default")

GCP_AUTOML_LOCATION = "us-central1"

DATA_SAMPLE_GCS_BUCKET_NAME = f"bucket_{DAG_ID}_{ENV_ID}".replace("_", "-")
RESOURCE_DATA_BUCKET = "airflow-system-tests-resources"

DATASET_NAME = f"ds_{DAG_ID}_{ENV_ID}".replace("-", "_")
DATASET = {
    "display_name": DATASET_NAME,
    "tables_dataset_metadata": {"target_column_spec_id": ""},
}
AUTOML_DATASET_BUCKET = f"gs://{DATA_SAMPLE_GCS_BUCKET_NAME}/automl/bank-marketing-split.csv"
IMPORT_INPUT_CONFIG = {"gcs_source": {"input_uris": [AUTOML_DATASET_BUCKET]}}
IMPORT_OUTPUT_CONFIG = {
    "gcs_destination": {"output_uri_prefix": f"gs://{DATA_SAMPLE_GCS_BUCKET_NAME}/automl"}
}

# change the name here
MODEL_NAME = f"md_{DAG_ID}_{ENV_ID}".replace("-", "_")
MODEL = {
    "display_name": MODEL_NAME,
    "tables_model_metadata": {"train_budget_milli_node_hours": 1000},
}

PREDICT_VALUES = [
    Value(string_value="TRAINING"),
    Value(string_value="51"),
    Value(string_value="blue-collar"),
    Value(string_value="married"),
    Value(string_value="primary"),
    Value(string_value="no"),
    Value(string_value="620"),
    Value(string_value="yes"),
    Value(string_value="yes"),
    Value(string_value="cellular"),
    Value(string_value="29"),
    Value(string_value="jul"),
    Value(string_value="88"),
    Value(string_value="10"),
    Value(string_value="-1"),
    Value(string_value="0"),
    Value(string_value="unknown"),
]


with DAG(
    dag_id=DAG_ID,
    schedule="@once",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example", "automl", "model"],
) as dag:
    create_bucket = GCSCreateBucketOperator(
        task_id="create_bucket",
        bucket_name=DATA_SAMPLE_GCS_BUCKET_NAME,
        storage_class="REGIONAL",
        location=GCP_AUTOML_LOCATION,
    )

    move_dataset_file = GCSSynchronizeBucketsOperator(
        task_id="move_data_to_bucket",
        source_bucket=RESOURCE_DATA_BUCKET,
        source_object="automl/datasets/model",
        destination_bucket=DATA_SAMPLE_GCS_BUCKET_NAME,
        destination_object="automl",
        recursive=True,
    )

    create_dataset = AutoMLCreateDatasetOperator(
        task_id="create_dataset",
        dataset=DATASET,
        location=GCP_AUTOML_LOCATION,
        project_id=GCP_PROJECT_ID,
    )

    dataset_id = create_dataset.output["dataset_id"]
    MODEL["dataset_id"] = dataset_id
    import_dataset = AutoMLImportDataOperator(
        task_id="import_dataset",
        dataset_id=dataset_id,
        location=GCP_AUTOML_LOCATION,
        input_config=IMPORT_INPUT_CONFIG,
    )

    # [START howto_operator_automl_create_model]
    create_model = AutoMLTrainModelOperator(
        task_id="create_model",
        model=MODEL,
        location=GCP_AUTOML_LOCATION,
        project_id=GCP_PROJECT_ID,
    )
    model_id = create_model.output["model_id"]
    # [END howto_operator_automl_create_model]

    # [START howto_operator_get_model]
    get_model = AutoMLGetModelOperator(
        task_id="get_model",
        model_id=model_id,
        location=GCP_AUTOML_LOCATION,
        project_id=GCP_PROJECT_ID,
    )
    # [END howto_operator_get_model]

    # [START howto_operator_prediction]
    predict_task = AutoMLPredictOperator(
        task_id="predict_task",
        model_id=model_id,
        payload={
            "row": {
                "values": PREDICT_VALUES,
            }
        },
        location=GCP_AUTOML_LOCATION,
        project_id=GCP_PROJECT_ID,
    )
    # [END howto_operator_prediction]

    # [START howto_operator_batch_prediction]
    batch_predict_task = AutoMLBatchPredictOperator(
        task_id="batch_predict_task",
        model_id=model_id,
        input_config=IMPORT_INPUT_CONFIG,
        output_config=IMPORT_OUTPUT_CONFIG,
        location=GCP_AUTOML_LOCATION,
        project_id=GCP_PROJECT_ID,
    )
    # [END howto_operator_batch_prediction]

    # [START howto_operator_automl_delete_model]
    delete_model = AutoMLDeleteModelOperator(
        task_id="delete_model",
        model_id=model_id,
        location=GCP_AUTOML_LOCATION,
        project_id=GCP_PROJECT_ID,
    )
    # [END howto_operator_automl_delete_model]

    delete_dataset = AutoMLDeleteDatasetOperator(
        task_id="delete_dataset",
        dataset_id=dataset_id,
        location=GCP_AUTOML_LOCATION,
        project_id=GCP_PROJECT_ID,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    delete_bucket = GCSDeleteBucketOperator(
        task_id="delete_bucket",
        bucket_name=DATA_SAMPLE_GCS_BUCKET_NAME,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    (
        # TEST SETUP
        [create_bucket >> move_dataset_file, create_dataset]
        >> import_dataset
        # TEST BODY
        >> create_model
        >> get_model
        >> predict_task
        >> batch_predict_task
        # TEST TEARDOWN
        >> delete_model
        >> delete_dataset
        >> delete_bucket
    )

    from tests.system.utils.watcher import watcher

    # This test needs watcher in order to properly mark success/failure
    # when "tearDown" task with trigger rule is part of the DAG
    list(dag.tasks) >> watcher()


from tests.system.utils import get_test_run  # noqa: E402

# Needed to run the example DAG with pytest (see: tests/system/README.md#run_via_pytest)
test_run = get_test_run(dag)
