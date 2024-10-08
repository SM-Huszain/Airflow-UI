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
import { useQuery } from "react-query";

import { getMetaValue } from "src/utils";
import type { API } from "src/types";
import type { DAG, DAGDetail } from "src/types/api-generated";
import useDag from "./useDag";

const dagDetailsApiUrl = getMetaValue("dag_details_api");

const combineResults = (
  dagData: DAG,
  dagDetailsData: DAGDetail
): Omit<DAGDetail, "defaultView"> => ({ ...dagData, ...dagDetailsData });

const useDagDetails = () => {
  const { data: dagData } = useDag();
  const dagDetailsResult = useQuery(
    ["dagDetailsQuery"],
    () => axios.get<AxiosResponse, API.DAGDetail>(dagDetailsApiUrl),
    {
      enabled: !!dagData,
    }
  );
  return {
    ...dagDetailsResult,
    data: combineResults(
      dagData || {},
      dagDetailsResult.data ? dagDetailsResult.data : {}
    ),
  };
};

export default useDagDetails;
