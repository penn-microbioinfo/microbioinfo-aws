#!/bin/bash

GO_VERSION=go1.23.1
osudo apt-get install bison
bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
gvm install ${GO_VERSION}
gvm use ${GO_VERSION} --default

