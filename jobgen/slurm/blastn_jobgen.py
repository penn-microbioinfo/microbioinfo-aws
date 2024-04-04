import re
import scriptgen
import os
import cellranger_command
import mbiaws
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--db")
parser.add_argument("--fasta_dir")
args = parser.parse_args()

db = args.db
fasta_dir = args.fasta_dir
setup_cmds = [
        "source /shared-ebs/source_me.bash",
        "export BLASTDB=/blastdb"]
for i,p in enumerate(os.listdir(fasta_dir)):
    sg = scriptgen.SlurmScriptGenerator(
            jobname=f"blastn_{i}",
            nodes=1,
            tasks_per_node=1,
            cpus_per_task=8,
            mem=48,
            time=168,
            partition="r5ad2x"
            )

    for sc in setup_cmds:
        sg.add_command(sc)

    sg.add_command(f'blastn -query {os.path.join(fasta_dir, p)} -db {db} -outfmt "$OUTFMT" -evalue 1e-10 -out {os.path.basename(p)}.blastout -max_target_seqs 5 -num_threads 8')
    sg.write()
