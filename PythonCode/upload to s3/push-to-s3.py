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

# Specify the S3 object key (file name) for push and pull
s3_object_key = 'vulnerability_scan_results.txt'

# Create an S3 client using the retrieved AWS credentials and region
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_default_region)

def push_to_s3(file_content):
    try:
        # Upload the file content to the specified S3 bucket and object key
        s3.put_object(Bucket=s3_bucket_name, Key=s3_object_key, Body=file_content)
        print(f"File pushed to S3: s3://{s3_bucket_name}/{s3_object_key}")
    except Exception as e:
        print(f"Error pushing to S3: {str(e)}")


if __name__ == "__main__":
    # Example content to push to S3
    content_to_push = "Example content to push to S3"

    # Push the content to S3
    push_to_s3(content_to_push)

    
