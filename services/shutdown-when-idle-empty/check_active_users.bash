#!/bin/bash

w -hs | grep -E "[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+" | tr -s ' ' | cut -d ' ' -f4 | tr '\n', ',' | sed 's/,$//'
