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

RUN git clone https://github.com/gnuaspell/aspell.git $SRC/aspell && cd $SRC/aspell && \
    git checkout e0646f9b063b23754951f1254f1ecb7af8ca36f3
RUN git clone -b master https://github.com/gnuaspell/aspell-fuzz.git $SRC/aspell-fuzz
RUN cd $SRC/aspell-fuzz && git checkout fa4aa32c6bf9573801a7675137e1c31b9f13247f

WORKDIR $SRC/aspell-fuzz
COPY build.sh $SRC/
COPY aspell_fuzzer.cpp $SRC/
