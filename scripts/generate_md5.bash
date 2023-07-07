#!/bin/bash

for i in $(ls *.fastq.gz); do
	if [ ! -f ${i}.md5_local ]; then
		md5sum $i > ${i}.md5_local
	fi
done
