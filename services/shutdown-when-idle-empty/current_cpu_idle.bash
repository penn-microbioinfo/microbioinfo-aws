#!/bin/bash
mpstat -u -P ALL 1 1 | grep -v Average | grep -v CPU | grep -v all | grep -vE '^$' | grep -Eo '[0-9.]+$'
