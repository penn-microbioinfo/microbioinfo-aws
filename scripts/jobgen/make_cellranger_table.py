import boto3
import sys
import argparse
import re
import os

def s3_get_object_keys(Bucket, Prefix):
    client = boto3.client("s3")
    paginator = client.get_paginator("list_objects")
    pages = paginator.paginate(Bucket = Bucket, Prefix = Prefix)
    for page in pages:
        for obj in page["Contents"]:
            yield obj["Key"]

def object_key_matches(pattern, objkey):
    s = re.search(pattern, objkey)
    if s is not None:
        return True
    else:
        return False

def object_read_number(pattern, objkey):
    s = re.search(pattern, os.path.basename(objkey))
    if s is not None:
        if len(s.groups()) > 1:
            raise ValueError(f"More than one matching read number: {objkey}")
        else:
            return s.group(1)
    else:
        raise ValueError(f"No matching read number: {objkey}")

# This function defaults to assuming that the protocol type is present in the second underscore-separated
# column of the file name, which should be the case if using `make_sample_sheet.bash` 
def object_protocol_type(fname, sep = "_", pos = 1, protocol_converter = None):
    protocol = fname.split(sep)[pos]
    if protocol_converter is not None:
        assert isinstance(protocol_converter, dict), "protocol_converter passed to object_protocol_type needs to be type dict"
        try:
            return protocol_converter[protocol]
        except KeyError:
            raise
    else:
        return protocol

emtab_style_protocol_converter = {
        "RNA": "scRNA-seq",
        "VDJ": "scVDJ-seq",
        "ADT": "scADT-seq",
        "snRNA-seq": "scADT-seq"
        }

parser = argparse.ArgumentParser()
parser.add_argument("--bucket", required = True)
parser.add_argument("--prefix", required = True)
parser.add_argument("--pattern", required = True)
args = parser.parse_args()

p = re.compile(args.pattern)
read_num_pat=re.compile("[_](R[0-9])[_]")
for k in s3_get_object_keys(args.bucket, args.prefix):
    if object_key_matches(p, k):
        key_parts = os.path.split(k)
        print("\t".join([object_protocol_type(key_parts[1], protocol_converter = emtab_style_protocol_converter), key_parts[1], object_read_number(read_num_pat,k), key_parts[0]]))
