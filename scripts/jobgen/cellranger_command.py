from collections import namedtuple
import os
import argparse
import sys
import re
import csv

''' for EMTAB sheets
coldict = {
        9: "protocol",
        10: "filename",
        11: "read_index",
        14: "awsdir"
        }
'''
DelimRow = namedtuple("DelimRow", ["protocol", "filename", "read_index", "awsdir"])

def cellranger_table_column_dict(protocol: int = 0, filename: int = 1, read_index: int = 2, awsdir: int = 3):
    coldict = {
            protocol: "protocol",
            filename: "filename",
            read_index: "read_index",
            awsdir: "awsdir"
            }
    return coldict

def cellranger_count_cmd(fastq_dir, ref, id, sample, include_introns = False, localcores = 1, localmem = 8, chemistry = "auto"):
    return f"cellranger count --fastqs {fastq_dir} --transcriptome {ref} --id {id} --sample {sample} --include-introns {str(include_introns).lower()} --localcores {localcores} --localmem {localmem} --chemistry {chemistry}"

def cellranger_commands(table, coldict = cellranger_table_column_dict(), key_prefix = "cellranger_matrices"):
    cmds = {}
    with open(table) as tsv:
        for line in tsv:
            this_sample = []
            row = newDelimRow(line.strip(), coldict)
            if not row.read_index in ["R1", "read1"]:
                continue
            if not row.protocol in ["snRNA-seq", "scRNA-seq"]:
                continue
            else:
                if row.protocol == "snRNA-seq":
                    ii = True
                else:
                    ii = False
            sampleid = re.sub("_S[0-9]+[_]L[0-9]+[_][IR][0-9]+[_][0-9]+[.]fastq[.]gz", "", row.filename)
            this_sample.append(f"python /shared-ebs/microbioinfo-aws/scripts/s3-download-multi.py --bucket microbioinfo-storage --prefix {os.path.join(row.awsdir, sampleid)} --chunksize 1.024e8 --pattern '[_]R[0-9]+[_][0-9]+[.]fastq[.]gz$' && \\")
            this_sample.append(cellranger_count_cmd("fastqs", "/cellranger-human-ref/refdata-gex-GRCh38-2020-A", sampleid, sampleid, include_introns = ii, localcores = 8, localmem=58) + " && \\") #+ f" && mv {sampleid}/outs/filtered_feature_bc_matrix /shared-ebs/cellranger_matrices/{sampleid}_filtered_feature_bc_matrix\n") <-- don't do this second part anymore - upload to S3 instead

            archive_name = f"{sampleid}_filtered_feature_bc_matrix.tar"
            this_sample.append(f"tar cvf {archive_name} {sampleid}/outs/filtered_feature_bc_matrix && \\")
            this_sample.append(f"python /shared-ebs/microbioinfo-aws/scripts/s3-multipart-upload.py --bucket microbioinfo-storage --key {key_prefix}/{archive_name} --partsize 100000000 --nproc 8 --largefile {archive_name}")
            if sampleid in cmds:
                assert this_sample == cmds[sampleid]
            else:
                cmds[sampleid] = this_sample

    return cmds

def newDelimRow(row, coldict, delim = '\t'):
    spl = row.split(delim)
    cols = []
    for i in coldict:
        cols.append(spl[i])
    return DelimRow._make(tuple(cols))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", required = True)
    parser.add_argument("--r1_filename", required = False)
    args = parser.parse_args()


