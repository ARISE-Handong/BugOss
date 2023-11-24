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
RUN apt-get update && apt-get install -y make autoconf automake libtool \
  pkg-config cmake nasm
RUN git clone https://github.com/DanBloomberg/leptonica.git leptonica && cd leptonica && \
    git checkout 8fc49016cf44ecbbab28979442e2781bd064584e
RUN git clone https://github.com/madler/zlib.git zlib
RUN cd $SRC/zlib && git reset --hard cacf7f1d4e3d44d871b605da3b647f07d718623f
RUN git clone https://gitlab.com/libtiff/libtiff libtiff
RUN cd $SRC/libtiff && git reset --hard 1373f8dacb47d0e256889172c6a5a6dc606f00ba
RUN git clone https://github.com/glennrp/libpng.git libpng
RUN cd $SRC/libpng && git reset --hard dbe3e0c43e549a1602286144d94b0666549b18e6
RUN git clone https://chromium.googlesource.com/webm/libwebp libwebp
RUN cd $SRC/libwebp && git reset --hard def64e920ff69e1d8270a2787d13df7c0d38d8ba
RUN git clone https://www.cl.cam.ac.uk/~mgk25/git/jbigkit jbigkit
RUN cd $SRC/jbigkit && git reset --hard 0e5b77e81aff2b377eb55bd5df09e1ab9e1ae63c
RUN git clone https://github.com/libjpeg-turbo/libjpeg-turbo libjpeg-turbo
RUN cd $SRC/libjpeg-turbo && git reset --hard 6ee5d5f568fda1a7c6a49dd8995f2d89866ee42d
RUN git clone https://github.com/facebook/zstd zstd
RUN cd $SRC/zstd && git reset --hard 8f8bd2d1ac555ac7b6f6bcfd67ba0a426f5a8309
WORKDIR leptonica
COPY build.sh $SRC/
COPY pix4_fuzzer.cc $SRC/
