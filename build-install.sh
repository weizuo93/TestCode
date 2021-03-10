#!/bin/sh

set -e

curdir=`dirname "$0"`
curdir=`cd "$curdir"; pwd`
export GLOG_DIR=$curdir

# thirdparties will be downloaded and unpacked here
export GLOG_SOURCE_DIR=$GLOG_DIR/src
# thirdparties will be installed to here
export GLOG_INSTALL_DIR=$GLOG_DIR/installed
# header files of all thirdparties will be intalled to here
export GLOG_INCLUDE_DIR=$GLOG_INSTALL_DIR/include
# libraries of all thirdparties will be intalled to here
export GLOG_LIB_DIR=$GLOG_INSTALL_DIR/lib

check_if_source_exist() {
    if [ -z $1 ]; then
        echo "dir should specified to check if exist."
        exit 1
    fi

    if [ ! -d $1 ];then
        echo "$1 does not exist."
        exit 1
    fi
    echo "===== begin build $1"
}

# gflags
build_and_install_gflags() {
    check_if_source_exist $GLOG_SOURCE_DIR/gflags-2.2.0
    cd $GLOG_SOURCE_DIR/gflags-2.2.0

    mkdir -p build && cd build
    rm -rf CMakeCache.txt CMakeFiles/
    cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX=$GLOG_INSTALL_DIR \
    -DCMAKE_POSITION_INDEPENDENT_CODE=On ../
    make -j$PARALLEL && make install
}

# glog
build_and_install_glog() {
    check_if_source_exist $GLOG_SOURCE_DIR/glog-0.3.3
    cd $GLOG_SOURCE_DIR/glog-0.3.3

    # to generate config.guess and config.sub to support aarch64
    rm -rf config.*
    autoreconf -i

    CPPFLAGS="-I${GLOG_INCLUDE_DIR} -fpermissive -fPIC" \
    LDFLAGS="-L${GLOG_LIB_DIR}" \
    CFLAGS="-fPIC" \
    ./configure --prefix=$GLOG_INSTALL_DIR --enable-frame-pointers --disable-shared --enable-static
    make -j$PARALLEL && make install
}

build_and_install_gflags

build_and_install_glog

echo "===== Finished to build and install glog ====="