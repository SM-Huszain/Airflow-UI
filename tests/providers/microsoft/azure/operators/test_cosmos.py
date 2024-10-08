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
from __future__ import annotations

import uuid
from unittest import mock

import pytest

from airflow.models import Connection
from airflow.providers.microsoft.azure.operators.cosmos import AzureCosmosInsertDocumentOperator


class TestAzureCosmosDbHook:
    # Set up an environment to test with
    @pytest.fixture(autouse=True)
    def setup_test_cases(self, create_mock_connection):
        # set up some test variables
        self.test_end_point = "https://test_endpoint:443"
        self.test_master_key = "magic_test_key"
        self.test_database_name = "test_database_name"
        self.test_collection_name = "test_collection_name"
        self.test_partition_key = "test_partition_key"
        create_mock_connection(
            Connection(
                conn_id="azure_cosmos_test_key_id",
                conn_type="azure_cosmos",
                login=self.test_end_point,
                password=self.test_master_key,
                extra={
                    "database_name": self.test_database_name,
                    "collection_name": self.test_collection_name,
                    "partition_key": self.test_partition_key,
                },
            )
        )

    @mock.patch("airflow.providers.microsoft.azure.hooks.cosmos.CosmosClient")
    def test_insert_document(self, cosmos_mock):
        test_id = str(uuid.uuid4())
        cosmos_mock.return_value.CreateItem.return_value = {"id": test_id}
        op = AzureCosmosInsertDocumentOperator(
            database_name=self.test_database_name,
            collection_name=self.test_collection_name,
            document={"id": test_id, "data": "sometestdata"},
            azure_cosmos_conn_id="azure_cosmos_test_key_id",
            task_id="azure_cosmos_sensor",
        )

        expected_calls = [
            mock.call()
            .get_database_client("test_database_name")
            .get_container_client("test_collection_name")
            .upsert_item({"data": "sometestdata", "id": test_id})
        ]

        op.execute(None)
        cosmos_mock.assert_any_call(self.test_end_point, {"masterKey": self.test_master_key})
        cosmos_mock.assert_has_calls(expected_calls)
