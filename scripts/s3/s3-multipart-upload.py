import boto3
import io
import botocore
import json
import argparse
import subprocess
import os
import logging
import re
import sys
import hashlib
import base64
import time
from multiprocessing import Pool

PARTS_FNAME_PATTERN="^x[a-z]{2}$"

class S3MultiPartUpload(object):
    def __init__(self, bucket, key, abort_on_failure_to_complete = False, nproc = 1):
        self.client = boto3.client("s3")
        self.bucket = bucket
        self.key = key
        self.upload_id = None
        self.part_fnames = None
        self.part_digests = None
        self.etag = None
        self.abort_on_failure_to_complete = abort_on_failure_to_complete
        self.nproc = nproc

        self.upload_id = self._create_upload()

    def _create_upload(self):
        return self.client.create_multipart_upload(Bucket = self.bucket, Key = self.key)["UploadId"]
    def _upload_part(self, partnumber, partpath, parthash):
        start = time.time()
        with open(partpath, 'rb') as fopen:
            try:
                self.client.upload_part(Bucket = self.bucket, Key = self.key, UploadId = self.upload_id, PartNumber = partnumber, Body = fopen, ContentMD5 = parthash)
            except botocore.exceptions.ClientError:
                self._abort()
                raise
        logging.info(f"Uploaded part #{partnumber}: {partpath} - {time.time()-start} seconds")

    def upload_parts(self, part_fnames):
        self.part_fnames = part_fnames
        logging.info(f"Part filenames (IN THIS ORDER): {self.part_fnames}")
        self.part_digests = S3MultiPartUpload._md5_digest_parts(self.part_fnames)
        parts = zip(range(1, len(self.part_fnames)+1), self.part_fnames, S3MultiPartUpload._encode_b64(self.part_digests)
)
        with Pool(self.nproc) as p:
            p.map(self._upload_part, parts)
    
    def _generate_etag (self):
        if self.part_fnames is not None and self.part_digests is not None:
            self.etag =  f"{md5hash( io.BytesIO(b''.join(self.part_digests)) ).hexdigest()}-{len(self.part_digests)}"
        else:
            raise ValueError("Cannot generate ETag without parts.")
    
    def _matches_etag(self, other_etag):
        if self.etag == other_etag:
            return True
        else:
            return False

    def _encode_b64(part_digests):
        return [base64.b64encode(x).decode("utf-8") for x in part_digests]
    
    def _md5_digest_parts(part_fnames):
        return [md5hash(open(x, 'rb')).digest() for x in part_fnames]

    def list_parts(self):
        try:
            r = self.client.list_parts(Bucket = self.bucket, Key = self.key, UploadId = self.upload_id)
        except botocore.exceptions.ClientError:
            self._abort()
            raise
        return r["Parts"]

    def complete_upload(self):
        self._generate_etag()

        #check list_parts against stored parts()

        multiparts = {"Parts": [{"PartNumber": p["PartNumber"], "ETag": p["ETag"]} for p in self.list_parts()]}

        try:
            r = self.client.complete_multipart_upload(Bucket = self.bucket, Key = self.key, UploadId = self.upload_id, MultipartUpload=multiparts) 
        except:
            self._abort()
        remote_etag = r["ETag"].replace('"', '') 
        if not self._matches_etag(remote_etag):
            logging.critical(f"Local and remote ETags do not match: {self.etag}")
            if self.abort_on_failure_to_complete:
                self._abort()
            else:
                logging.critical(f"Unable to complete MultipartUpload. It will have to be done manually:\n{'-'*25}\naws s3api complete-multipart-upload --bucket {self.bucket} --key {self.key} --upload-id {self.upload_id} --multipart-upload {multiparts}")

    def _abort(self):
        if self.upload_id is None:
            logging.critical("Unable to abort prior to creation.")
            raise ValueError
        try:
            self.client.abort_multipart_upload(Bucket = self.bucket, Key = self.key, UploadId = self.upload_id)
            logger.critical("Upload aborted successfully.")
        except botocore.exceptions.ClientError:
            logging.critical(f"Unable to abort MultipartUpload. It will have to be done manually:\n{'-'*25}\naws s3api abort-multipart-upload --bucket {self.bucket} --key {self.key} --upload-id {self.upload_id}")
            raise

def get_upload_id(response):
    return response["UploadId"]

def make_file_parts(largefile, part_size = 4950000000, parts_outdir = None): 
    cmd = ["split", "-b", str(part_size), largefile] 
    p = subprocess.run(cmd, capture_output = True)
    try:
        p.check_returncode()
    except subprocess.CalledProcessError:
        logging.critical(f"Call to `split` failed with: {p.stderr}")
        sys.exit(1)

    pat = re.compile(PARTS_FNAME_PATTERN)
    part_fnames = [x for x in os.listdir(".") if re.match(pat, x)]
    
    # This sort is very important, becasue python reads the file names out
    # of sort order
    part_fnames.sort()
    
    check_file_part_sizes(largefile, part_fnames)

    return part_fnames

def check_file_part_sizes(largefile, part_fnames):
    file_part_sizes = [os.stat(x).st_size for x in part_fnames]
    file_parts_total_size = sum(file_part_sizes)
    largefile_size = os.stat(largefile).st_size
    if file_parts_total_size != largefile_size:
        logging.critical(f"Sum of file part sizes is not equal to file size. {file_parts_total_size} != {largefile_size}")
        sys.exit(1)

def md5hash(f, block_size = 2**20):
    md5 = hashlib.new("md5")
    while True:
        block = f.read(block_size)
        if not block:
            break
        md5.update(block)
    return md5


def check_final_etag(local_etag, remote_etag):
    if local_etag != remote_etag:
        logging.critical(f"Local ETag does not equal remote ETag: {local_etag} != {remote_etag}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bucket", action = "store", help = "")
    parser.add_argument("-k", "--key", action = "store", help = "")
    parser.add_argument("-s", "--partsize", action = "store", help = "", default = 4950000000)
    parser.add_argument("-f", "--largefile", action = "store", help = "")
    parser.add_argument("-p", "--nproc", action = "store", type = int, help = "")
    args = parser.parse_args()

    part_fnames = make_file_parts(args.largefile, part_size = args.partsize)

    # Begin interactions with S3
    mpu = S3MultiPartUpload(args.bucket, args.key, nproc = args.npro)
    mpu.upload_parts(part_fnames)
    mpu.complete_upload()


    

