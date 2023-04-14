# Copyright 2019 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################

FROM gcr.io/oss-fuzz-base/base-builder
MAINTAINER weinrank@fh-muenster.de
RUN apt-get update && apt-get install -y make cmake
RUN git clone --branch oss-fuzz https://github.com/weinrank/usrsctp usrsctp && cd usrsctp && \
    git checkout 05bea46702687f26a81c41c3fb1fd1dd3d9c0aa1
WORKDIR usrsctp
COPY build.sh $SRC/
COPY CMakeLists.txt $SRC/
COPY fuzzer_connect.c $SRC/
