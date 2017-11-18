import boto
import boto3
import boto.s3
import botocore

from boto.s3.key import Key

import os.path
import sys

# Fill these in - you get them when you sign up for S3
AWS_ACCESS_KEY_SECRET = 'S6Yz2L1a4/aJq4Th5Mrts4ddbX0gmHLPKIfHsDIO'
AWS_ACCESS_KEY_ID = 'AKIAJMENREMHZ4LTTHXA'
# Fill in info on data to upload
# destination bucket name
bucket_name = 'dump-fileit-client-2016-as-of-20170413'
#bucket_name = "sample"
# source directory
sourceDir = '/Users/vino/workspace/documentClassifier/SharedFile/Test/'
# destination directory name (on s3)
destDir = 'client/'

#max size in bytes before uploading in parts. between 1 and 5 GB recommended
MAX_SIZE = 20 * 1000 * 1000
#size of parts when uploading in parts
PART_SIZE = 6 * 1000 * 1000

s3= boto3.resource("s3")
exist = False

conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY_SECRET)
print(conn)
bucket = conn.get_bucket(bucket_name)

# # bucket = conn.create_bucket(bucket_name,
#     location=boto.s3.connection.Location.DEFAULT)

# print(bucket)
print("-----Connection Established")
uploadFileNames = []


def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

for (sourceDir, dirname, filename) in os.walk(sourceDir):

    for f in filename:
        sourcepath = os.path.abspath(os.path.join(sourceDir, f))
        print(sourcepath)
        print("Uploading {} to Amazon S3 bucket {} ".format(sourcepath, bucket_name))
        filesize = os.path.getsize(sourcepath)
        print(filesize)
        destpath = sourcepath.replace("/Users/vino/workspace/documentClassifier/SharedFile", "")
        print(destpath)
        # import pdb;pdb.set_trace()
        k = Key(bucket, destpath)

        if(k.exists()):
            print("File Already Exists.....")
            continue
        else:
            print("File Does not exist")
            if filesize > MAX_SIZE:
                print("multipart upload")
                mp = bucket.initiate_multipart_upload(destpath)
                fp = open(sourcepath,'rb')
                fp_num = 0
                while (fp.tell() < filesize):
                    fp_num += 1
                    print("uploading part %i" %fp_num)
                    mp.upload_part_from_file(fp, fp_num, cb=percent_cb, num_cb=10, size=PART_SIZE)

                mp.complete_upload()

            else:
                print("singlepart upload")
                destpath = sourcepath.replace("/Users/vino/workspace/documentClassifier/SharedFile","")
                print(destpath)
                k = boto.s3.key.Key(bucket)
                k.key = destpath
                k.set_contents_from_filename(sourcepath,
                    cb=percent_cb, num_cb=10)

