"""
<this error when uploading a <zip file 
tutorial-env) osboxes@osboxes:~/tutorial-env/bin$ python3 'AWS push-pull updated.py' /home/osboxes/awscliv2.zip Tyrone 
Traceback (most recent call last):
  File "/home/osboxes/tutorial-env/bin/AWS push-pull updated.py", line 49, in <module>
    content_to_push = file.read()
                      ^^^^^^^^^^^
  File "<frozen codecs>", line 322, in decode
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa6 in position 10: invalid start byte
"""


import argparse

import boto3

from configparser import ConfigParser



# Load AWS credentials from the configuration file

configure = ConfigParser()

configure.read('aws-configure.ini')



# Retrieve AWS credentials and S3 bucket details from the configuration file

aws_access_key_id = configure.get('default', 'aws_access_key_id')

aws_secret_access_key = configure.get('default', 'aws_secret_access_key')

aws_default_region = configure.get('default', 'region')

s3_bucket_name = configure.get('default', 's3_bucket_name')



# Specify the base folder in the S3 bucket

base_folder = 'Reports/'



# Create an S3 client using the retrieved AWS credentials and region

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_default_region)



def push_to_s3(file_content, file_name, client_name):

    try:

        # Customize the S3 object key based on the folder, file name, and client name

        s3_object_key = f'{base_folder}{client_name}/{file_name}'



        # Upload the file content to the specified S3 bucket and object key

        s3.put_object(Bucket=s3_bucket_name, Key=s3_object_key, Body=file_content)

        print(f"File pushed to S3: s3://{s3_bucket_name}/{s3_object_key}")

    except Exception as e:

        print(f"Error pushing to S3: {str(e)}")



if __name__ == "__main__":

    # Setup argparse to handle command line arguments

    parser = argparse.ArgumentParser(description="Push content to S3 with file name and client name.")

    parser.add_argument("file_name", help="Name of the file to push to S3.")

    parser.add_argument("client_name", help="Name of the client.")



    # Parse the command line arguments

    args = parser.parse_args()



    # Read content of file being pushed to S3

    with open(args.file_name, 'rb') as file:

        content_to_push = file.read()



    # Push the content to S3 with the provided file name and client name

    push_to_s3(content_to_push, args.file_name, args.client_name)
