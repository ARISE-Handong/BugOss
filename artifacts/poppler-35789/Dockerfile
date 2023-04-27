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

FROM gcr.io/oss-fuzz-base/base-builder
RUN apt-get update && apt-get install -y wget autoconf automake libtool pkg-config gperf
RUN pip3 install meson ninja

RUN git clone https://github.com/madler/zlib.git zlib
RUN cd zlib && git checkout cacf7f1d4e3d44d871b605da3b647f07d718623f && cd ../
RUN git clone git://git.sv.nongnu.org/freetype/freetype2.git freetype2
RUN cd freetype2 && git checkout d3dc2da9b27af5b90575d62989389cc65fe7977c && cd ../
RUN git clone https://github.com/mm2/Little-CMS.git Little-CMS
RUN cd Little-CMS && git checkout bcd0f282e71de26e267ce61de27fb4d493cbda56 && cd ../
RUN git clone https://github.com/uclouvain/openjpeg openjpeg
RUN cd openjpeg && git checkout cc1919b183f76d5ac79cc9927fb899b47700d925 && cd ../
RUN git clone https://github.com/glennrp/libpng.git libpng
RUN cd libpng && git checkout a37d4836519517bdce6cb9d956092321eca3e73b && cd ../
RUN git clone https://gitlab.freedesktop.org/fontconfig/fontconfig.git fontconfig
RUN cd fontconfig && git checkout e291fda7d42e5d64379555097a066d9c2c4efce3 && cd ../
RUN git clone https://gitlab.freedesktop.org/cairo/cairo.git cairo
RUN cd cairo && git checkout 0eff09a1e3a7b035d01c739320bc87ae1077b57e && cd ../
RUN git clone git://code.qt.io/qt/qtbase.git qtbase
RUN cd qtbase && git checkout ffa0ecdc5d507754ddd962e2edbc859c198b2700 && cd ../
RUN git clone https://gitlab.gnome.org/GNOME/pango.git pango
RUN cd pango && git checkout b7c7eb7a7c80d8df18ac2c97fb03dbbfaf0686cb && cd ../
ADD https://ftp.gnome.org/pub/gnome/sources/glib/2.64/glib-2.64.2.tar.xz $SRC
RUN tar xvJf $SRC/glib-2.64.2.tar.xz
RUN wget https://boostorg.jfrog.io/artifactory/main/release/1.76.0/source/boost_1_76_0.tar.bz2
RUN git clone --single-branch https://gitlab.freedesktop.org/poppler/poppler.git poppler && \
    cd poppler && git checkout 2b2808719d2c91283ae358381391bb0b37d9061d

RUN git clone https://github.com/mozilla/pdf.js pdf.js && cd pdf.js && \
    git checkout d80651e5724686535ac4fbdfac5d5e280a16dbdb && \
    zip -q $SRC/poppler_seed_corpus.zip $SRC/pdf.js/test/pdfs/*.pdf && \
    rm -rf pdf.js

ADD https://raw.githubusercontent.com/google/fuzzing/master/dictionaries/pdf.dict $SRC/poppler.dict
WORKDIR $SRC/poppler
COPY build.sh $SRC/
COPY label_fuzzer.cc $SRC/
