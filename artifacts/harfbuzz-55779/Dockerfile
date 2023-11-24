# Copyright 2016 Google Inc.
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
RUN apt-get update && apt-get install -y python3-pip ragel pkg-config && \
    pip3 install meson==0.56.0 ninja
RUN git clone https://github.com/harfbuzz/harfbuzz.git $SRC/harfbuzz && cd $SRC/harfbuzz && \
	git checkout 8708b9e081192786c027bb7f5f23d76dbe5c19e8 
WORKDIR harfbuzz
COPY build.sh hb-shape-fuzzer.cc $SRC/
