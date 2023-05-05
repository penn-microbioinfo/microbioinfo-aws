import argparse
import logging
import boto3
from pathos.multiprocessing import ProcessPool
from pathos.helpers import cpu_count

def list_files(bucket, prefix):
    olist = boto3.client("s3").list_objects(Bucket = bucket, Prefix = prefix)

    if "Contents" in olist:
        return olist["Contents"]
    else:
        raise OSError(f"`{prefix}` does not match any objects in bucket `{bucket}`")

def _get_file(key):
    getobj = boto3.client("s3").get_object(Bucket = bucket, Key = key)

    

def get_files(keylist, nproc = cpu_count()):
    with ProcessPool(nodes = nproc) as p:
        p.map(_get_file, keylist)

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket", action = "store", help = "")
    parser.add_argument("-k", "--prefix", action = "store", help = "Prefix for objects to download (i.e., the bucket directory).")
    parser.add_argument("-p", "--nproc", action = "store", default = cpu_count(), type = int, help = "")
    args = parser.parse_args()

    get_files([x["Key"] for x in list_files(args.bucket, args.prefix)])



