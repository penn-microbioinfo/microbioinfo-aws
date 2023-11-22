#!/bin/bash
#SBATCH --job-name=s3cp
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=48
#SBATCH --nodelist=r5ad2x-dy-r5ad12xlarge-2
#SBATCH --mem-per-cpu=32g
#SBATCH --time=168:00:00
#SBATCH --partition=r5ad2x

source /shared-ebs/source_me.bash
for d in $(ls -d /local-ebs/humann_out/*/); do
	sn=$(basename $d)
	aws s3 cp $d/${sn}_combined_humann_temp/${sn}_combined.log s3://upenn-research.thaiss-lab-psom-01.us-east-1/humann/humann_out/$sn/${sn}_combined.log
done
