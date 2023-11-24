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

RUN apt-get update && apt-get install -y gcc g++ make cmake flex bison
RUN git clone https://github.com/seladb/PcapPlusPlus PcapPlusPlus && cd PcapPlusPlus && \
    git checkout 50aab202d24331ef35b9eff68d96ef9f97baf6a1

# Get tcpdump's test pcaps as seed corpus
RUN git clone https://github.com/the-tcpdump-group/tcpdump.git tcpdump && cd tcpdump && git checkout ea4e272785eb3a1aab6ac148f178439c86aa68ae
RUN git clone https://github.com/the-tcpdump-group/libpcap.git libpcap && cd libpcap && git checkout 35bfb718dc84ff9beac6bb3e0c9c817a12dee3f8

WORKDIR PcapPlusPlus

COPY build.sh $SRC
COPY *.options $SRC
COPY FuzzTarget.cpp $SRC
