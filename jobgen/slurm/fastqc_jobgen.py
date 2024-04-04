import re
import scriptgen
import os
import cellranger_command
import mbiaws
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--bucket")
parser.add_argument("--prefix")
args = parser.parse_args()

prefix = args.prefix
bucket = args.bucket
readfiles = []
for i in mbiaws.s3.lib.list_object_keys(bucket, prefix):
    if mbiaws.s3.lib.object_key_matches("R[0-9][_][0-9]+[.]fastq[.]gz$", i):
        readfiles.append(i)
setup_cmds = ["source /shared-ebs/source_me.bash",
              "REPO=/shared-ebs/microbioinfo-aws/scripts/",
              "unset AWS_PROFILE; unset AWS_SHARED_CREDENTIALS_FILE", # Make sure boto3 used IAM profile creds
              "mkdir -p /local-ebs/fastqc/",
              "cd /local-ebs/fastqc"]
fastqc_s3_out = os.path.join(os.path.dirname(prefix), "fastqc") 
for i,p in enumerate(readfiles):
    sg = scriptgen.SlurmScriptGenerator(
            jobname=f"fastqc_{i}",
            nodes=1,
            tasks_per_node=1,
            cpus_per_task=1,
            mem=7,
            time=168,
            partition="r5ad2x"
            )

    for sc in setup_cmds:
        sg.add_command(sc)

    s3_uri = f"s3://{os.path.join(bucket, p)}"
    rpt = os.path.basename(p).replace(".fastq.gz", "_fastqc.html")
    #out = os.path.join(fastqc_s3_out, )
    sg.add_command(f"aws s3 cp {s3_uri} .")
    sg.add_command(f"fastqc {os.path.basename(p)}")
    sg.add_command(f"cp {rpt} /shared-ebs/betts_fastqc/.")
    sg.write()
