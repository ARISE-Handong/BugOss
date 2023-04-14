#!/bin/bash -eu
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

mv $SRC/fuzz_htp.c $SRC/libhtp/test/fuzz
mv $SRC/fuzz_htp.h $SRC/libhtp/test/fuzz

CXXFLAGS=$(echo $CXXFLAGS | sed 's/\-O1/\-O0/g')
CFLAGS=$(echo $CFLAGS | sed 's/\-O1/\-O0/g')
export CXXFLAGS=$CXXFLAGS
export CFLAGS=$CFLAGS

# build project
cd libhtp

sed -i 's/OLEVEL=2/OLEVEL=0/g' configure.ac 

sh autogen.sh
./configure
make

$CC $CFLAGS -I. -c test/fuzz/fuzz_htp.c -o fuzz_htp.o
$CC $CFLAGS -I. -c test/test.c -o test.o
$CXX $CXXFLAGS fuzz_htp.o test.o -o $OUT/fuzz_htp ./htp/.libs/libhtp.a $LIB_FUZZING_ENGINE -lz -llzma

# builds corpus
#zip -r $OUT/fuzz_htp_seed_corpus.zip test/files/*.t
