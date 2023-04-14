#!/bin/bash -eu
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

mv $SRC/grk_decompress_fuzzer.cpp $SRC/grok/tests/fuzzers/

CXXFLAGS=$(echo $CXXFLAGS | sed 's/\-O1/\-O0/g')
CFLAGS=$(echo $CFLAGS | sed 's/\-O1/\-O0/g')
export CXXFLAGS=$CXXFLAGS
export CFLAGS=$CFLAGS

mkdir build
cd build
cmake ..

sed -i 's/O1/O0/g' CMakeCache.txt
sed -i 's/O2/O0/g' CMakeCache.txt
sed -i 's/O3/O0/g' CMakeCache.txt

make clean -s
make -j$(nproc) -s
cd ..

./tests/fuzzers/build_google_oss_fuzzers.sh
#./tests/fuzzers/build_seed_corpus.sh
