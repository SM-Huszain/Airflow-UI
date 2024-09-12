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
"""
DebugExecutor.

.. seealso::
    For more information on how the DebugExecutor works, take a look at the guide:
    :ref:`executor:DebugExecutor`
"""

from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING, Any

from airflow.executors.base_executor import BaseExecutor
from airflow.utils.state import TaskInstanceState

if TYPE_CHECKING:
    from airflow.models.taskinstance import TaskInstance
    from airflow.models.taskinstancekey import TaskInstanceKey


class DebugExecutor(BaseExecutor):
    """
    This executor is meant for debugging purposes. It can be used with SQLite.

    It executes one task instance at time. Additionally to support working
    with sensors, all sensors ``mode`` will be automatically set to "reschedule".
    """

    _terminated = threading.Event()

    is_single_threaded: bool = True
    is_production: bool = False

    change_sensor_mode_to_reschedule: bool = True

    def __init__(self):
        super().__init__()
        self.tasks_to_run: list[TaskInstance] = []
        # Place where we keep information for task instance raw run
        self.tasks_params: dict[TaskInstanceKey, dict[str, Any]] = {}
        from airflow.configuration import conf

        self.fail_fast = conf.getboolean("debug", "fail_fast")

    def execute_async(self, *args, **kwargs) -> None:
        """Replace the method with a custom trigger_task implementation."""

    def sync(self) -> None:
        task_succeeded = True
        while self.tasks_to_run:
            ti = self.tasks_to_run.pop(0)
            if self.fail_fast and not task_succeeded:
                self.log.info("Setting %s to %s", ti.key, TaskInstanceState.UPSTREAM_FAILED)
                ti.set_state(TaskInstanceState.UPSTREAM_FAILED)
                self.change_state(ti.key, TaskInstanceState.UPSTREAM_FAILED)
            elif self._terminated.is_set():
                self.log.info("Executor is terminated! Stopping %s to %s", ti.key, TaskInstanceState.FAILED)
                ti.set_state(TaskInstanceState.FAILED)
                self.fail(ti.key)
            else:
                task_succeeded = self._run_task(ti)

    def _run_task(self, ti: TaskInstance) -> bool:
        self.log.debug("Executing task: %s", ti)
        key = ti.key
        try:
            params = self.tasks_params.pop(ti.key, {})
            ti.run(job_id=ti.job_id, **params)
            self.success(key)
            return True
        except Exception as e:
            ti.set_state(TaskInstanceState.FAILED)
            self.fail(key)
            self.log.exception("Failed to execute task: %s.", e)
            return False

    def queue_task_instance(
        self,
        task_instance: TaskInstance,
        mark_success: bool = False,
        pickle_id: int | None = None,
        ignore_all_deps: bool = False,
        ignore_depends_on_past: bool = False,
        wait_for_past_depends_before_skipping: bool = False,
        ignore_task_deps: bool = False,
        ignore_ti_state: bool = False,
        pool: str | None = None,
        cfg_path: str | None = None,
    ) -> None:
        """Queues task instance with empty command because we do not need it."""
        if TYPE_CHECKING:
            assert task_instance.task

        self.queue_command(
            task_instance,
            [str(task_instance)],  # Just for better logging, it's not used anywhere
            priority=task_instance.priority_weight,
            queue=task_instance.task.queue,
        )
        # Save params for TaskInstance._run_raw_task
        self.tasks_params[task_instance.key] = {
            "mark_success": mark_success,
            "pool": pool,
        }

    def trigger_tasks(self, open_slots: int) -> None:
        """
        Triggers tasks.

        Instead of calling exec_async we just add task instance to tasks_to_run queue.

        :param open_slots: Number of open slots
        """
        if not self.queued_tasks:
            # wait a bit if there are no tasks ready to be executed to avoid spinning too fast in the void
            time.sleep(0.5)
            return

        sorted_queue = sorted(
            self.queued_tasks.items(),
            key=lambda x: x[1][1],
            reverse=True,
        )
        for _ in range(min((open_slots, len(self.queued_tasks)))):
            key, (_, _, _, ti) = sorted_queue.pop(0)
            self.queued_tasks.pop(key)
            self.running.add(key)
            self.tasks_to_run.append(ti)  # type: ignore

    def end(self) -> None:
        """Set states of queued tasks to UPSTREAM_FAILED marking them as not executed."""
        for ti in self.tasks_to_run:
            self.log.info("Setting %s to %s", ti.key, TaskInstanceState.UPSTREAM_FAILED)
            ti.set_state(TaskInstanceState.UPSTREAM_FAILED)
            self.change_state(ti.key, TaskInstanceState.UPSTREAM_FAILED)

    def terminate(self) -> None:
        self._terminated.set()
