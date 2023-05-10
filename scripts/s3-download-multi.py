import argparse
import os
import logging
import boto3
import codecs
from pathos.multiprocessing import ProcessPool
from pathos.helpers import cpu_count

def list_files(bucket, prefix):
    olist = boto3.client("s3").list_objects(Bucket = bucket, Prefix = prefix)

    if "Contents" in olist:
        return olist["Contents"]
    else:
        raise OSError(f"`{prefix}` does not match any objects in bucket `{bucket}`")

def _get_file(key, bucket, chunksize = 1.024e6):
    getobj = boto3.client("s3").get_object(Bucket = bucket, Key = key)
    base = os.path.basename(key)
    if os.path.isfile(base):
        pass
    else:
        with open(base, 'wb') as local:
            for chunk in getobj["Body"].iter_chunks():
                local.write(chunk)
    

def get_files(keylist, bucket, nproc, chunksize = 1.024e6):
    buckets = [bucket]*len(keylist)
    with ProcessPool(nodes = nproc) as p:
        p.map(_get_file, keylist, buckets)

if __name__ == "__main__":
    # Python > 3.8
    #logging.basicConfig(encoding='utf-8', level=logging.INFO)
    # Python <= 3.8
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket", action = "store", help = "")
    parser.add_argument("--overwrite", action = "store_true", help = "Overwrite files that exist. Default: skip over")
    parser.add_argument("-k", "--prefix", action = "store", help = "Prefix for objects to download (i.e., the bucket directory).")
    parser.add_argument("-p", "--nproc", action = "store", default = cpu_count(), type = int, help = "")
    parser.add_argument("--chunksize",  action = "store", default = 1.024e6, type = float, help = "")
    args = parser.parse_args()

    get_files([x["Key"] for x in list_files(args.bucket, args.prefix)], args.bucket, nproc=args.nproc, chunksize=args.chunksize)



