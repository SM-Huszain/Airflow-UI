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

from unittest import mock

from google.api_core.gapic_v1.method import DEFAULT
from google.cloud.videointelligence_v1 import AnnotateVideoResponse, Feature

from airflow.providers.google.cloud.operators.video_intelligence import (
    CloudVideoIntelligenceDetectVideoExplicitContentOperator,
    CloudVideoIntelligenceDetectVideoLabelsOperator,
    CloudVideoIntelligenceDetectVideoShotsOperator,
)

PROJECT_ID = "project-id"
GCP_CONN_ID = "gcp-conn-id"
IMPERSONATION_CHAIN = ["ACCOUNT_1", "ACCOUNT_2", "ACCOUNT_3"]
CONFIG = {"encoding": "LINEAR16"}
AUDIO = {"uri": "gs://bucket/object"}

INPUT_URI = "gs://test-bucket//test-video.mp4"


class TestCloudVideoIntelligenceOperators:
    @mock.patch("airflow.providers.google.cloud.operators.video_intelligence.CloudVideoIntelligenceHook")
    def test_detect_video_labels_green_path(self, mock_hook):
        mocked_operation = mock.Mock()
        mocked_operation.result = mock.Mock(return_value=AnnotateVideoResponse(annotation_results=[]))
        mock_hook.return_value.annotate_video.return_value = mocked_operation

        CloudVideoIntelligenceDetectVideoLabelsOperator(
            input_uri=INPUT_URI,
            task_id="id",
            gcp_conn_id=GCP_CONN_ID,
            impersonation_chain=IMPERSONATION_CHAIN,
        ).execute(context={"task_instance": mock.Mock()})

        mock_hook.assert_called_once_with(
            gcp_conn_id=GCP_CONN_ID,
            impersonation_chain=IMPERSONATION_CHAIN,
        )
        mock_hook.return_value.annotate_video.assert_called_once_with(
            input_uri=INPUT_URI,
            features=[Feature.LABEL_DETECTION],
            input_content=None,
            video_context=None,
            location=None,
            retry=DEFAULT,
            timeout=None,
        )

    @mock.patch("airflow.providers.google.cloud.operators.video_intelligence.CloudVideoIntelligenceHook")
    def test_detect_video_explicit_content_green_path(self, mock_hook):
        mocked_operation = mock.Mock()
        mocked_operation.result = mock.Mock(return_value=AnnotateVideoResponse(annotation_results=[]))
        mock_hook.return_value.annotate_video.return_value = mocked_operation

        CloudVideoIntelligenceDetectVideoExplicitContentOperator(
            input_uri=INPUT_URI,
            task_id="id",
            gcp_conn_id=GCP_CONN_ID,
            impersonation_chain=IMPERSONATION_CHAIN,
        ).execute(context={"task_instance": mock.Mock()})

        mock_hook.assert_called_once_with(
            gcp_conn_id=GCP_CONN_ID,
            impersonation_chain=IMPERSONATION_CHAIN,
        )
        mock_hook.return_value.annotate_video.assert_called_once_with(
            input_uri=INPUT_URI,
            features=[Feature.EXPLICIT_CONTENT_DETECTION],
            input_content=None,
            video_context=None,
            location=None,
            retry=DEFAULT,
            timeout=None,
        )

    @mock.patch("airflow.providers.google.cloud.operators.video_intelligence.CloudVideoIntelligenceHook")
    def test_detect_video_shots_green_path(self, mock_hook):
        mocked_operation = mock.Mock()
        mocked_operation.result = mock.Mock(return_value=AnnotateVideoResponse(annotation_results=[]))
        mock_hook.return_value.annotate_video.return_value = mocked_operation

        CloudVideoIntelligenceDetectVideoShotsOperator(
            input_uri=INPUT_URI,
            task_id="id",
            gcp_conn_id=GCP_CONN_ID,
            impersonation_chain=IMPERSONATION_CHAIN,
        ).execute(context={"task_instance": mock.Mock()})

        mock_hook.assert_called_once_with(
            gcp_conn_id=GCP_CONN_ID,
            impersonation_chain=IMPERSONATION_CHAIN,
        )
        mock_hook.return_value.annotate_video.assert_called_once_with(
            input_uri=INPUT_URI,
            features=[Feature.SHOT_CHANGE_DETECTION],
            input_content=None,
            video_context=None,
            location=None,
            retry=DEFAULT,
            timeout=None,
        )
