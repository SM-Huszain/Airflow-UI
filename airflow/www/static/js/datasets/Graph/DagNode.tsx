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

import React from "react";
import {
  Button,
  Flex,
  Link,
  Popover,
  PopoverArrow,
  PopoverCloseButton,
  PopoverContent,
  PopoverFooter,
  PopoverHeader,
  PopoverTrigger,
  Portal,
  Text,
  useTheme,
} from "@chakra-ui/react";
import { MdOutlineAccountTree } from "react-icons/md";

import { useContainerRef } from "src/context/containerRef";
import { getMetaValue } from "src/utils";

const DagNode = ({
  dagId,
  isHighlighted,
  isSelected,
  onSelect,
}: {
  dagId: string;
  isHighlighted?: boolean;
  isSelected?: boolean;
  onSelect?: (dagId: string, type: string) => void;
}) => {
  const { colors } = useTheme();
  const containerRef = useContainerRef();

  const gridUrl = getMetaValue("grid_url").replace("__DAG_ID__", dagId);
  return (
    <Popover trigger="hover">
      <PopoverTrigger>
        <Flex
          borderColor={
            isHighlighted || isSelected ? colors.blue[400] : undefined
          }
          borderRadius={5}
          borderWidth={isSelected ? 4 : 2}
          fontWeight={isSelected ? "bold" : "normal"}
          p={2}
          height="100%"
          width="100%"
          cursor="pointer"
          fontSize={16}
          justifyContent="space-between"
          alignItems="center"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            if (onSelect) onSelect(dagId, "dag");
          }}
        >
          <MdOutlineAccountTree size="16px" />
          <Text ml={2}>{dagId}</Text>
        </Flex>
      </PopoverTrigger>
      <Portal containerRef={containerRef}>
        <PopoverContent bg="gray.100">
          <PopoverArrow bg="gray.100" />
          <PopoverCloseButton />
          <PopoverHeader>{dagId}</PopoverHeader>
          <PopoverFooter as={Flex} justifyContent="space-between">
            <Button
              as={Link}
              href={gridUrl}
              variant="outline"
              colorScheme="blue"
            >
              View DAG
            </Button>
          </PopoverFooter>
        </PopoverContent>
      </Portal>
    </Popover>
  );
};

export default DagNode;
