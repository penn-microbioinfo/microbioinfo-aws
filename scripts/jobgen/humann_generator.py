import scriptgen
import itertools
import numpy as np
import os
import argparse
import re
import boto3
import sys
import subprocess
import pathlib

def list_files(bucket, prefix):
    objnames = []
    objsizes = []
    pag = boto3.client("s3").get_paginator("list_objects")
    page_itr = pag.paginate(Bucket = bucket, Prefix = prefix)

    for page in page_itr:
        for i in page["Contents"]:
            objnames.append(i["Key"])
            objsizes.append(i["Size"])
    return list(zip(objnames, objsizes))

BUCKET="upenn-research.thaiss-lab-psom-01.us-east-1"
PROT_DB="/local-ebs/db/uniref90"
CHOC_DB="/local-ebs/db/chocophlan"
META_DB="/local-ebs/db/metaphlan"
BTIDX = "mpa_vOct22_CHOCOPhlAnSGB_202212"
NUMTHREADS = 12
SAMP_PER_CHUNK=4

to_run = [x.strip() for x in open("/shared-ebs/humann_prep/seq_IDs_to_run_on_aws_n2203_230926.txt").readlines()]
#to_run = ["ELSGYLCD", "FNSRFOBB", "PSNNKAEH", "QUUBZBFR", "LIMZSXSX", "NWTDWUIF"]
#to_run = ["AAFJPMKZ","AANRMCHE","AAZWCHIN","ABNGXNOE","ABPUIWML","ABSBIHCS","ABSQNHKU","ABVHWLHB","ABVLBKYM","ABWWCACL","ABXJGSZN","ACGIZVJC"]
#to_run = ["AANRMCHE", "ABSQNHKU", "AMQOKHBS"]
response = list_files(BUCKET, prefix="humann/fastq/")
response = [x for x in response if x[0].endswith(".fastq.gz")]
fp,fs = zip(*response)
fp = [pathlib.Path(x) for x in fp]
fs = sorted(list(enumerate(fs)), key=lambda indexed_size: indexed_size[1], reverse=True)
fp = [fp[x[0]] for x in fs]
aws_completed =list(set([pathlib.Path(x[0]).parts[2] for x in list_files(BUCKET, prefix="humann/humann_out")]))
samples = [re.sub("[_]R[0-9]+.fastq.gz", "", x.name) for x in fp]
seen = set()
samples = [x for x in samples if not (x in seen or seen.add(x))]
samples = [x for x in samples if x in to_run and x not in aws_completed]
print(samples)
print(len(samples))
print(len(set(samples)))
nchunks = np.ceil(np.true_divide(len(samples), SAMP_PER_CHUNK))

for jsi,chunk in enumerate(np.array_split(samples, nchunks)):
    sg = scriptgen.SlurmScriptGenerator(
            jobname=f"humann_{jsi}",
            nodes=1,
            tasks_per_node=1,
            cpus_per_task=48,
            mem=180,
            time=168,
            partition="m6id,m5ad"
            )
    sg.add_command("source /shared-ebs/source_me.bash")
    sg.add_command("conda activate humann37")
    sg.add_command("cd /local-ebs")
    sg.add_command(f"mkdir -p {CHOC_DB}")
    sg.add_command(f"cd {CHOC_DB}")
    sg.add_command(f"python /shared-ebs/microbioinfo-aws/scripts/s3-download-multi.py -b {BUCKET} -k humann/chocophlan_db/chocophlan/ -p {NUMTHREADS*SAMP_PER_CHUNK}")
    sg.add_command(f"mkdir -p {META_DB}")
    sg.add_command(f"cd {META_DB}")
    sg.add_command(f"python /shared-ebs/microbioinfo-aws/scripts/s3-download-multi.py -b {BUCKET} -k humann/metaphlan_db/{BTIDX}/ -p {NUMTHREADS*SAMP_PER_CHUNK}")
    sg.add_command(f"mkdir -p {PROT_DB}")
    sg.add_command(f"cd {PROT_DB}")
    sg.add_command("aws s3 cp s3://upenn-research.thaiss-lab-psom-01.us-east-1/humann/uniref90_db/uniref/uniref90_201901b_full.dmnd .")
    sg.add_command("cd /local-ebs")
    sg.add_command("mkdir -p /local-ebs/fastq/")
    sg.add_command("mkdir /local-ebs/humann_out")
    sg.add_command("cd /local-ebs/fastq")
    for sample in chunk:
        log_start = f"echo TIMESTAMP START {sample} $(date) && \\"
        pull = f"python /shared-ebs/microbioinfo-aws/scripts/s3-download-multi.py -b {BUCKET} -k humann/fastq/ -p {NUMTHREADS*SAMP_PER_CHUNK} --pattern '[/]{sample}_R[0-9][.]fastq[.]gz$' && \\"
        cat_reads = f"cat /local-ebs/fastq/{sample}_R1.fastq.gz /local-ebs/fastq/{sample}_R2.fastq.gz > /local-ebs/fastq/{sample}_combined.fastq.gz && \\"
        cd_to_humann_out = f"cd /local-ebs/humann_out && \\"
        run_humann = f"humann -i /local-ebs/fastq/{sample}_combined.fastq.gz -o /local-ebs/humann_out/{sample} --nucleotide-database {CHOC_DB} --protein-database {PROT_DB} --threads {NUMTHREADS} --memory-use maximum --metaphlan-options '--bowtie2db {META_DB} --index {BTIDX} --unclassified_estimation -t rel_ab --nproc {NUMTHREADS}' && \\"
        cd_to_sample_out = f"cd /local-ebs/humann_out/{sample} && \\"
        copy_bugs = f"cp {sample}_combined_humann_temp/{sample}_combined_metaphlan_bugs_list.tsv . && \\"
        push = f"for o in $(ls *.tsv); do aws s3 cp $o s3://upenn-research.thaiss-lab-psom-01.us-east-1/humann/humann_out/{sample}/$o; done && \\"
        push_log = f"aws s3 cp {sample}_combined_humann_temp/{sample}_combined.log s3://upenn-research.thaiss-lab-psom-01.us-east-1/humann/humann_out/{sample}_combined.log && \\"
        log_stop = f"echo TIMESTAMP STOP {sample} $(date) &"
        sg.add_command('\n'.join([f"    {x}" for x in [log_start, pull, cat_reads, cd_to_humann_out, run_humann, cd_to_sample_out, copy_bugs, push, push_log, log_stop]]))
        sg.add_command("")
        sg.add_command("")
    sg.add_command("wait")
    sg.add_command("cd /local-ebs/humann_out; while read logf; do aws s3 cp $logf s3://upenn-research.thaiss-lab-psom-01.us-east-1/humann/partial_logs/$(basename $logf); done < <(find . -name '*.log')")
    sg.add_command("cd /local-ebs; rm -r fastq humann_out db") 
    sg.write()
