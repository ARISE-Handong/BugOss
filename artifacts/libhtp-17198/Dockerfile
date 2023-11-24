# Copyright 2018 Google Inc.
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
RUN apt-get update && apt-get install -y make autoconf automake libtool zlib1g-dev liblzma-dev
RUN git clone https://github.com/OISF/libhtp.git libhtp && cd libhtp && \
    git checkout 3c6555078ec30e0baa4855ec69d55a22fc8d3589
WORKDIR $SRC
COPY build.sh $SRC/
COPY fuzz_htp.c fuzz_htp.h $SRC/
