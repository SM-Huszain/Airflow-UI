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

from typing import NamedTuple

from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from airflow.models.pool import Pool


class PoolSchema(SQLAlchemySchema):
    """Pool schema."""

    class Meta:
        """Meta."""

        model = Pool

    name = auto_field("pool")
    slots = auto_field()
    occupied_slots = fields.Method("get_occupied_slots", dump_only=True)
    running_slots = fields.Method("get_running_slots", dump_only=True)
    queued_slots = fields.Method("get_queued_slots", dump_only=True)
    scheduled_slots = fields.Method("get_scheduled_slots", dump_only=True)
    open_slots = fields.Method("get_open_slots", dump_only=True)
    deferred_slots = fields.Method("get_deferred_slots", dump_only=True)
    description = auto_field()
    # we skip auto_field() here to be compatible with the manual validation in the pool_endpoint module
    include_deferred = fields.Boolean(load_default=False)

    @staticmethod
    def get_occupied_slots(obj: Pool) -> int:
        """Return the occupied slots of the pool."""
        return obj.occupied_slots()

    @staticmethod
    def get_running_slots(obj: Pool) -> int:
        """Return the running slots of the pool."""
        return obj.running_slots()

    @staticmethod
    def get_queued_slots(obj: Pool) -> int:
        """Return the queued slots of the pool."""
        return obj.queued_slots()

    @staticmethod
    def get_scheduled_slots(obj: Pool) -> int:
        """Return the scheduled slots of the pool."""
        return obj.scheduled_slots()

    @staticmethod
    def get_deferred_slots(obj: Pool) -> int:
        """Return the deferred slots of the pool."""
        return obj.deferred_slots()

    @staticmethod
    def get_open_slots(obj: Pool) -> float:
        """Return the open slots of the pool."""
        return obj.open_slots()


class PoolCollection(NamedTuple):
    """List of Pools with metadata."""

    pools: list[Pool]
    total_entries: int


class PoolCollectionSchema(Schema):
    """Pool Collection schema."""

    pools = fields.List(fields.Nested(PoolSchema))
    total_entries = fields.Int()


pool_collection_schema = PoolCollectionSchema()
pool_schema = PoolSchema()
