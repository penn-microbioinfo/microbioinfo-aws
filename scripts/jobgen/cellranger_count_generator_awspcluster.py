import scriptgen
import numpy as np
import os
import argparse
import re
import cellranger_command

illumina_suffix = re.compile("[_]S[0-9]+[_]L[0-9]+[_]R[0-9][_][0-9]+[.]fastq[.]gz$")
r1_pat = re.compile("[_]R1[_]")

parser = argparse.ArgumentParser()
parser.add_argument("--table", required = True)
parser.add_argument("--splits", default = 1, type = int, help = "Number of job scripts to split jobs across.")
parser.add_argument("--s3_output_prefix", default = "cellranger_matrices", help = "Where to deposit cellranger output matrices on S3.")
args = parser.parse_args()


setup_cmds = ["source /shared-ebs/source_me.bash",
              "REPO=/shared-ebs/microbioinfo-aws/scripts/",
              #"export PATH=$PATH:/shared-ebs/bin", <- done soure_me.bash
              "mkdir -p /local-ebs/cellranger/fastqs",
              "cd /local-ebs/cellranger/fastqs && \\"]
for i,cmd_chunk in enumerate(np.array_split(list(cellranger_command.cellranger_commands(args.table, key_prefix = args.s3_output_prefix).values()), args.splits)):
    sg = scriptgen.SlurmScriptGenerator(
            jobname=f"crcount_{i}",
            nodes=1,
            tasks_per_node=1,
            cpus_per_task=8,
            mem=60,
            time=168,
            partition="r5ad"
            )
    for sc in setup_cmds:
        sg.add_command(sc)
    for sample in cmd_chunk:
        sg.add_command(sample[0])
        sg.add_command("cd /local-ebs/cellranger/ && \\")
        sg.add_command(sample[1])
        sg.add_command(sample[2])
        sg.add_command(sample[3])
    sg.write()
