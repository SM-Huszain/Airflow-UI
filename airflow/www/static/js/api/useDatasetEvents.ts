/*!
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

import axios from "axios";
import { useQuery, UseQueryOptions } from "react-query";

import { getMetaValue } from "src/utils";
import URLSearchParamsWrapper from "src/utils/URLSearchParamWrapper";
import type {
  DatasetEventCollection,
  GetDatasetEventsVariables,
} from "src/types/api-generated";

interface Props extends GetDatasetEventsVariables {
  options?: UseQueryOptions<DatasetEventCollection>;
}

const useDatasetEvents = ({
  datasetId,
  sourceDagId,
  sourceRunId,
  sourceTaskId,
  sourceMapIndex,
  limit,
  offset,
  orderBy,
  options,
}: Props) => {
  const query = useQuery<DatasetEventCollection>(
    [
      "datasets-events",
      datasetId,
      sourceDagId,
      sourceRunId,
      sourceTaskId,
      sourceMapIndex,
      limit,
      offset,
      orderBy,
    ],
    () => {
      const datasetsUrl = getMetaValue("dataset_events_api");

      const params = new URLSearchParamsWrapper();

      if (limit) params.set("limit", limit.toString());
      if (offset) params.set("offset", offset.toString());
      if (orderBy) params.set("order_by", orderBy);
      if (datasetId) params.set("dataset_id", datasetId.toString());
      if (sourceDagId) params.set("source_dag_id", sourceDagId);
      if (sourceRunId) params.set("source_run_id", sourceRunId);
      if (sourceTaskId) params.set("source_task_id", sourceTaskId);
      if (sourceMapIndex)
        params.set("source_map_index", sourceMapIndex.toString());

      return axios.get(datasetsUrl, {
        params,
      });
    },
    {
      keepPreviousData: true,
      ...options,
    }
  );
  return {
    ...query,
    data: query.data ?? { datasetEvents: [], totalEntries: 0 },
  };
};

export default useDatasetEvents;
