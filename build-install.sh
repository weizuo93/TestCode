#!/bin/sh

set -e

curdir=`dirname "$0"`
curdir=`cd "$curdir"; pwd`
export THRIFT_DIR=$curdir

# thirdparties will be downloaded and unpacked here
export THRIFT_SOURCE_DIR=$THRIFT_DIR/thrift
# thirdparties will be installed to here
export THRIFT_INSTALL_DIR=$THRIFT_DIR/installed
# header files of all thirdparties will be intalled to here
export THRIFT_INCLUDE_DIR=$THRIFT_INSTALL_DIR/include
# libraries of all thirdparties will be intalled to here
export THRIFT_LIB_DIR=$THRIFT_INSTALL_DIR/lib

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

# thrift
build_and_install_thrift() {
    check_if_source_exist $THRIFT_SOURCE_DIR/thrift-0.9.3
    cd $THRIFT_SOURCE_DIR/thrift-0.9.3

    if [ ! -f configure ]; then
        ./bootstrap.sh
    fi

    echo ${THRIFT_LIB_DIR}
    ./configure CPPFLAGS="-I${THRIFT_INCLUDE_DIR}" LDFLAGS="-L${THRIFT_LIB_DIR} -static-libstdc++ -static-libgcc" LIBS="-lcrypto -ldl -lssl" CFLAGS="-fPIC" \
    --prefix=$THRIFT_INSTALL_DIR --docdir=$THRIFT_INSTALL_DIR/doc --enable-static --disable-shared --disable-tests \
    --disable-tutorial --without-qt4 --without-qt5 --without-csharp --without-erlang --without-nodejs \
    --without-lua --without-perl --without-php --without-php_extension --without-dart --without-ruby \
    --without-haskell --without-go --without-haxe --without-d --with-python -with-java --with-cpp \
    --with-libevent=$THRIFT_INSTALL_DIR --with-boost=$THRIFT_INSTALL_DIR --with-openssl=$THRIFT_INSTALL_DIR

    if [ -f compiler/cpp/thrifty.hh ];then
        mv compiler/cpp/thrifty.hh compiler/cpp/thrifty.h
    fi

    echo "===== begin install thrift-0.9.3"

    make -j$PARALLEL && make install
}

build_and_install_thrift

echo "===== Finished to build and install thrift ====="