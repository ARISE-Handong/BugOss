# Copyright 2020 Google Inc.
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
RUN apt-get update && apt-get install -y wget

RUN git clone https://github.com/GrokImageCompression/grok.git grok && cd grok && \
    git checkout 93e6af95ec46bbba5e112a1fbdbdb6a1294d61d8
RUN git clone https://github.com/GrokImageCompression/grok-test-data.git grok/data && \
    cd grok/data && git checkout 5118df38d89d26949c82d9143c74d80656781089
WORKDIR grok
COPY build.sh $SRC/
COPY grk_decompress_fuzzer.cpp $SRC/
