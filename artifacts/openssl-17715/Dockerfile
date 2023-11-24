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
MAINTAINER kurt@roeckx.be
RUN apt-get update && apt-get install -y make
RUN git clone https://github.com/openssl/openssl.git openssl && cd openssl && \
    git checkout 4baee2d72e0c82bfd6de085df23a1bdc6af887ba
WORKDIR openssl
COPY build.sh *.options $SRC/
COPY fuzzer.h rand.inc x509.c $SRC/
