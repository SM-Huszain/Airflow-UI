#!/usr/bin/env python
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

import os
import sys
from glob import glob
from pathlib import Path

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))
ACCEPTED_NON_INIT_DIRS = ["adr", "doc", "templates"]


def check_dir_init_file(provider_files: list[str]) -> None:
    missing_init_dirs: list[Path] = []
    for candidate_path in provider_files:
        if candidate_path.endswith("/__pycache__"):
            continue
        path = Path(candidate_path)
        if path.is_dir() and not (path / "__init__.py").exists():
            if path.name not in ACCEPTED_NON_INIT_DIRS:
                missing_init_dirs.append(path)

    if missing_init_dirs:
        with open(os.path.join(ROOT_DIR, "scripts/ci/license-templates/LICENSE.txt")) as license:
            license_txt = license.readlines()
        prefixed_licensed_txt = [f"# {line}" if line != "\n" else "#\n" for line in license_txt]

        for missing_init_dir in missing_init_dirs:
            (missing_init_dir / "__init__.py").write_text("".join(prefixed_licensed_txt))

        print("No __init__.py file was found in the following provider directories:")
        print("\n".join([missing_init_dir.as_posix() for missing_init_dir in missing_init_dirs]))
        print("\nThe missing __init__.py files have been created. Please add these new files to a commit.")
        sys.exit(1)


if __name__ == "__main__":
    all_provider_subpackage_dirs = sorted(glob(f"{ROOT_DIR}/airflow/providers/**/*", recursive=True))
    check_dir_init_file(all_provider_subpackage_dirs)
    all_test_provider_subpackage_dirs = sorted(glob(f"{ROOT_DIR}/tests/providers/**/*", recursive=True))
    check_dir_init_file(all_test_provider_subpackage_dirs)
