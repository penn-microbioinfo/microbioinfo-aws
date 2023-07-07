#!/bin/bash

source /shared-ebs/source_me.bash
export PATH=$PATH:/shared-ebs/bin
REPO=/shared-ebs/microbioinfo-aws/scripts/

#python $REPO/create_ebs.py


#devname=$(lsblk | tail -n1 | cut -d ' ' -f1)
#sudo mkfs.ext4 /dev/${devname}
#sudo mkdir /local-ebs
#sudo mount /dev/${devname} /local-ebs
#sudo chown ubuntu /local-ebs

mkdir -p /local-ebs/cellranger/fastqs
cd /local-ebs/cellranger/fastqs

python $REPO/s3-download-multi.py --bucket microbioinfo-storage --nproc 4 --prefix simoni_ref/emtab_12421/Pla_HDBR8715514 --chunksize 1.024e8 

cd ../
cellranger count --fastqs fastqs --transcriptome /simoni-data/ref/refdata-gex-GRCh38-2020-A --id Pla_HDBR8715514 --sample Pla_HDBR8715514 --include-introns false --localcores 8 --localmem 58 --chemistry auto

mv Pla_HDBR8715514/outs/filtered_feature_bc_matrix /shared-ebs/cellranger_matrices/Pla_HDBR8715514_filtered_feature_bc_matrix

