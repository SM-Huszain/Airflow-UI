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

import axios, { AxiosResponse } from "axios";
import { useMutation, useQueryClient } from "react-query";

import URLSearchParamsWrapper from "src/utils/URLSearchParamWrapper";
import { getMetaValue } from "src/utils";
import { useAutoRefresh } from "src/context/autorefresh";
import useErrorToast from "src/utils/useErrorToast";

const csrfToken = getMetaValue("csrf_token");
const clearRunUrl = getMetaValue("dagrun_clear_url");

export default function useClearRun(dagId: string, runId: string) {
  const queryClient = useQueryClient();
  const errorToast = useErrorToast();
  const { startRefresh } = useAutoRefresh();
  return useMutation(
    ["dagRunClear", dagId, runId],
    ({
      confirmed = false,
      only_failed = false,
    }: {
      confirmed: boolean;
      only_failed?: boolean;
    }) => {
      const params = new URLSearchParamsWrapper({
        csrf_token: csrfToken,
        confirmed,
        only_failed,
        dag_id: dagId,
        dag_run_id: runId,
      }).toString();

      return axios.post<AxiosResponse, string[]>(clearRunUrl, params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });
    },
    {
      onSuccess: (_, { confirmed }) => {
        if (confirmed) {
          queryClient.invalidateQueries("gridData");
          startRefresh();
        }
      },
      onError: (error: Error) => errorToast({ error }),
    }
  );
}
