import scriptgen
import numpy as np
import os
import argparse
import re

illumina_suffix = re.compile("[_]S[0-9]+[_]L[0-9]+[_]R[0-9][_][0-9]+[.]fastq[.]gz$")
r1_pat = re.compile("[_]R1[_]")

parser = argparse.ArgumentParser()
parser.add_argument("--pattern", required = False, help = "Quoted python regular expresion pattern to match filenames for upload.")
parser.add_argument("--local_dir", required = False, help = "Path to directory containing files.")
parser.add_argument("--remote_dir", required = False, help = "Path-style directory key for remote.")
parser.add_argument("--splits", default = 1, type = int, help = "Number of job scripts to split jobs across.")
parser.add_argument("-b", "--bucket", action = "store", help = "")
parser.add_argument("-s", "--partsize", action = "store", help = "", default = 4950000000)
parser.add_argument("-p", "--nproc", action = "store", required=True, type = int, help = "")
args = parser.parse_args()

p = re.compile(args.pattern)

for i,flist in enumerate(np.array_split([x for x in os.listdir(args.local_dir) if re.search(p, x) is not None], args.splits)):
    sg = scriptgen.SlurmScriptGenerator(
            jobname=f"s3up_{i}",
            nodes=1,
            tasks_per_node=1,
            cpus_per_task=4,
            mem=6,
            time=168,
            partition="m6a"
            )
    for f in flist:
        sg.add_command(f"python /shared-ebs/microbioinfo-aws/scripts/s3-multipart-upload.py --bucket {args.bucket} --key {os.path.join(args.remote_dir, f)} --partsize {args.partsize} --largefile {os.path.join(args.local_dir, f)} --nproc {args.nproc}")
    sg.write()
