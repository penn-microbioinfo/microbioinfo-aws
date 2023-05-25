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
        print("\t".join(["scRNA-seq", key_parts[1], object_read_number(read_num_pat,k), key_parts[0]]))
