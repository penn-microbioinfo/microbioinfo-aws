#!/bin/bash
RAW=/home/ec2-user/scratch/raw
FILT=/home/ec2-user/scratch/cbfilt
LOGS=/home/ec2-user/scratch/logs
sample_name_pat="^[0-9]+[_][0-9]+[a-z]*"
for sn in $(ls $RAW | grep -oE $sample_name_pat); do
	inputf=$RAW/${sn}_raw_feature_bc_matrix.h5 
	outputf=$FILT/${sn}_cbfilt_feature_bc_matrix.h5	
	echo $sn
	cellbender remove-background --input $inputf --output $outputf --exclude-feature-types "Antibody Capture" --cuda 2>&1 | tee $LOGS/${sn}_cellbender.log
done
