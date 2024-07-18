#!/bin/bash

if [ -z $PREFIX ]; then
    PREFIX=$HOME
fi
BUILD_DIR=$PREFIX/build

if [ ! -d $BUILD_DIR ]; then
    mkdir $BUILD_DIR
fi

cd $BUILD_DIR
wget https://www.python.org/ftp/python/3.12.1/Python-3.12.1.tgz
tar xvfz Python-3.12.1.tgz
rm Python-3.12.1.tgz
cd Python-3.12.1
./configure --prefix=$PREFIX --enable-optimizations --with-openssl=/usr --enable-loadable-sqlite-extensions=yes
make
sudo make altinstall 
sudo rm -rf $BUILD_DIR/Python-3.12.1
sudo ln -s $PREFIX/bin/python3.12 $PREFIX/bin/python3
sudo ln -s $PREFIX/bin/pip3.12 $PREFIX/bin/pip3
