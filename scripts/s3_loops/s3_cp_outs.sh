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
	cp $d/${sn}_combined_humann_temp/${sn}_combined_metaphlan_bugs_list.tsv $d/.
	for out in $(ls $d/*.tsv); do
		aws s3 cp $out s3://upenn-research.thaiss-lab-psom-01.us-east-1/humann/humann_out/$sn/$(basename $out)
	done
done
