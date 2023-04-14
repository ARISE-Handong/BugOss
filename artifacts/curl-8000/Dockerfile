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

FROM gcr.io/oss-fuzz-base/base-builder

RUN git clone https://github.com/curl/curl.git $SRC/curl && cd $SRC/curl && \
    git checkout dd7521bcc1b7a6fcb53c31f9bd1192fcc884bd56

RUN git clone https://github.com/curl/curl-fuzzer.git $SRC/curl_fuzzer
RUN cd $SRC/curl_fuzzer && git reset --hard c4ce63bf55674cebdad03f8bb6adb354bfc63609

# Use curl-fuzzer's scripts to get latest dependencies.
RUN $SRC/curl_fuzzer/scripts/ossfuzzdeps.sh

WORKDIR $SRC/curl
COPY build.sh curl_fuzzer.cc $SRC/
