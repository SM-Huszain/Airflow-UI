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

import stat

from airflow_breeze.utils.run_utils import (
    change_directory_permission,
    change_file_permission,
)


def test_change_file_permission(tmp_path):
    tmpfile = tmp_path / "test.config"
    tmpfile.write_text("content")
    change_file_permission(tmpfile)
    mode = tmpfile.stat().st_mode
    assert not (mode & stat.S_IWGRP)
    assert not (mode & stat.S_IWOTH)


def test_change_directory_permission(tmp_path):
    subdir = tmp_path / "testdir"
    subdir.mkdir()
    change_directory_permission(subdir)
    mode = subdir.stat().st_mode
    assert not (mode & stat.S_IWGRP)
    assert not (mode & stat.S_IWOTH)
    assert mode & stat.S_IXGRP
    assert mode & stat.S_IXOTH
