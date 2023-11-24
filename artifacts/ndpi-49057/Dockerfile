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

FROM gcr.io/oss-fuzz-base/base-builder@sha256:66fb5b08c6f1f93db5ceabac066c11054f6034664ecb750a9278cf74a07ce96e
RUN apt-get update && apt-get install -y make autoconf automake autogen pkg-config libtool flex bison cmake
RUN git clone --depth 1 https://github.com/json-c/json-c.git json-c
RUN git clone https://github.com/ntop/nDPI.git ndpi && cd ndpi && \
    git checkout 2edfaeba4ada90ca8771a44132d2b9cc85e45570
ADD https://www.tcpdump.org/release/libpcap-1.9.1.tar.gz libpcap-1.9.1.tar.gz

COPY build.sh $SRC/
COPY fuzz_process_packet.c $SRC/
WORKDIR $SRC
