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

from typing import TYPE_CHECKING

from deprecated import deprecated

from airflow.exceptions import AirflowProviderDeprecationWarning
from airflow.providers.yandex.hooks.yandex import YandexCloudBaseHook

if TYPE_CHECKING:
    from yandexcloud._wrappers.dataproc import Dataproc


class DataprocHook(YandexCloudBaseHook):
    """
    A base hook for Yandex.Cloud Data Proc.

    :param yandex_conn_id: The connection ID to use when fetching connection info.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cluster_id = None
        self.dataproc_client: Dataproc = self.sdk.wrappers.Dataproc(
            default_folder_id=self.default_folder_id,
            default_public_ssh_key=self.default_public_ssh_key,
        )

    @property
    @deprecated(
        reason="`client` deprecated and will be removed in the future. Use `dataproc_client` instead",
        category=AirflowProviderDeprecationWarning,
    )
    def client(self):
        return self.dataproc_client

    @client.setter
    def client(self, value):
        self.dataproc_client = value
