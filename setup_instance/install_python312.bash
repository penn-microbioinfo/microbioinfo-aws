#!/bin/bash

SHARED_HOME=/shared-ebs
BUILD_DIR=$SHARED_HOME/builds

if [ ! -d $BUILD_DIR ]; then
    mkdir $BUILD_DIR
fi

cd $BUILD_DIR
wget https://www.python.org/ftp/python/3.12.1/Python-3.12.1.tgz
tar xvfz Python-3.12.1.tgz
rm Python-3.12.1.tgz
cd Python-3.12.1
./configure --prefix=$SHARED_HOME --enable-optimizations
make
sudo make altinstall 
