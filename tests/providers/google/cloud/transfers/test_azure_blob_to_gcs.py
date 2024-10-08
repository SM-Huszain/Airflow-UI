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
from __future__ import annotations

from unittest import mock

from airflow.providers.google.cloud.transfers.azure_blob_to_gcs import AzureBlobStorageToGCSOperator

WASB_CONN_ID = "wasb_default"
GCP_CONN_ID = "google_cloud_default"
BLOB_NAME = "azure_blob"
CONTAINER_NAME = "azure_container"
BUCKET_NAME = "airflow"
OBJECT_NAME = "file.txt"
FILENAME = "file.txt"
GZIP = False
IMPERSONATION_CHAIN = None
TASK_ID = "transfer_file"


class TestAzureBlobStorageToGCSTransferOperator:
    def test_init(self):
        operator = AzureBlobStorageToGCSOperator(
            wasb_conn_id=WASB_CONN_ID,
            gcp_conn_id=GCP_CONN_ID,
            blob_name=BLOB_NAME,
            container_name=CONTAINER_NAME,
            bucket_name=BUCKET_NAME,
            object_name=OBJECT_NAME,
            filename=FILENAME,
            gzip=GZIP,
            impersonation_chain=IMPERSONATION_CHAIN,
            task_id=TASK_ID,
        )
        assert operator.wasb_conn_id == WASB_CONN_ID
        assert operator.blob_name == BLOB_NAME
        assert operator.container_name == CONTAINER_NAME
        assert operator.gcp_conn_id == GCP_CONN_ID
        assert operator.bucket_name == BUCKET_NAME
        assert operator.object_name == OBJECT_NAME
        assert operator.filename == FILENAME
        assert operator.gzip == GZIP
        assert operator.impersonation_chain == IMPERSONATION_CHAIN
        assert operator.task_id == TASK_ID

    @mock.patch("airflow.providers.google.cloud.transfers.azure_blob_to_gcs.WasbHook")
    @mock.patch("airflow.providers.google.cloud.transfers.azure_blob_to_gcs.GCSHook")
    @mock.patch("airflow.providers.google.cloud.transfers.azure_blob_to_gcs.tempfile")
    def test_execute(self, mock_temp, mock_hook_gcs, mock_hook_wasb):
        op = AzureBlobStorageToGCSOperator(
            wasb_conn_id=WASB_CONN_ID,
            gcp_conn_id=GCP_CONN_ID,
            blob_name=BLOB_NAME,
            container_name=CONTAINER_NAME,
            bucket_name=BUCKET_NAME,
            object_name=OBJECT_NAME,
            filename=FILENAME,
            gzip=GZIP,
            impersonation_chain=IMPERSONATION_CHAIN,
            task_id=TASK_ID,
        )

        op.execute(context=None)
        mock_hook_wasb.assert_called_once_with(wasb_conn_id=WASB_CONN_ID)

        mock_hook_wasb.return_value.get_file.assert_called_once_with(
            file_path=mock_temp.NamedTemporaryFile.return_value.__enter__.return_value.name,
            container_name=CONTAINER_NAME,
            blob_name=BLOB_NAME,
        )
        mock_hook_gcs.assert_called_once_with(
            gcp_conn_id=GCP_CONN_ID, impersonation_chain=IMPERSONATION_CHAIN
        )
        mock_hook_gcs.return_value.upload.assert_called_once_with(
            bucket_name=BUCKET_NAME,
            object_name=OBJECT_NAME,
            gzip=GZIP,
            filename=mock_temp.NamedTemporaryFile.return_value.__enter__.return_value.name,
        )

    @mock.patch("airflow.providers.google.cloud.transfers.azure_blob_to_gcs.WasbHook")
    def test_execute_single_file_transfer_openlineage(self, mock_hook_wasb):
        from airflow.providers.common.compat.openlineage.facet import Dataset

        MOCK_AZURE_ACCOUNT_NAME = "mock_account_name"
        mock_hook_wasb.return_value.get_conn.return_value.account_name = MOCK_AZURE_ACCOUNT_NAME

        operator = AzureBlobStorageToGCSOperator(
            wasb_conn_id=WASB_CONN_ID,
            gcp_conn_id=GCP_CONN_ID,
            blob_name=BLOB_NAME,
            container_name=CONTAINER_NAME,
            bucket_name=BUCKET_NAME,
            object_name=OBJECT_NAME,
            filename=FILENAME,
            gzip=GZIP,
            impersonation_chain=IMPERSONATION_CHAIN,
            task_id=TASK_ID,
        )

        lineage = operator.get_openlineage_facets_on_start()

        assert len(lineage.inputs) == 1
        assert len(lineage.outputs) == 1
        assert lineage.inputs[0] == Dataset(
            namespace=f"wasbs://{CONTAINER_NAME}@{MOCK_AZURE_ACCOUNT_NAME}", name=BLOB_NAME
        )
        assert lineage.outputs[0] == Dataset(namespace=f"gs://{BUCKET_NAME}", name=OBJECT_NAME)
