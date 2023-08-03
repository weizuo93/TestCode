#!/usr/bin/env bash
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

set -e

ROOT=`dirname "$0"`
ROOT=`cd "$ROOT"; pwd`

export PROJECT_HOME=$ROOT

mvn clean package -DskipTests

echo "Build JavaPluginMain ..."

PROJECT_OUTPUT=${PROJECT_HOME}/output/
rm -rf ${PROJECT_OUTPUT}
mkdir ${PROJECT_OUTPUT}
cp ${PROJECT_HOME}/target/simple-plugin-main-thread.zip ${PROJECT_HOME}/output/

cd ${PROJECT_HOME}/output/
unzip simple-plugin-main-thread.zip
mkdir plugins

echo "Build JavaPluginMain Finished"
