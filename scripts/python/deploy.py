#!/usr/bin/env python
import configparser
import boto3
import botocore
from datetime import datetime
import pytz

config = configparser.ConfigParser()
config.read('aws.config.properties')

accessKey = config.get('AWS', 'aws.access.key')
secretKey = config.get('AWS', 'aws.secret.key')
bucket_path = config.get('DEPLOYMENT', 'deploy.artifact.s3.path.bucket')
module_ui_path = config.get('DEPLOYMENT', 'deploy.artifact.s3.path.ui')
module_graphql_path = config.get('DEPLOYMENT', 'deploy.artifact.s3.path.graphql')
module_py_path = config.get('DEPLOYMENT', 'deploy.artifact.s3.path.py')

client = boto3.client(
    's3',
    aws_access_key_id=accessKey,
    aws_secret_access_key=secretKey
)
response = client.list_buckets()

for bucket in response['Buckets']:
	print bucket["Name"]

def get_latest_artifact(bucket, prefix, saving_file_name):
	uiartifacts = client.list_objects(Bucket=bucket, Prefix=prefix)
	uiartifact_contents = uiartifacts['Contents']
	latest_artifact = sorted(uiartifact_contents, key=lambda x: x['LastModified'], reverse=True)[0]
	print 'Latest build artifact: %s'%(latest_artifact['Key'])
	client.download_file(bucket, latest_artifact['Key'], saving_file_name)
	
get_latest_artifact(bucket_path, module_ui_path, '/var/temp/aws/alphaoneui.zip')
get_latest_artifact(bucket_path, module_graphql_path, '/var/temp/aws/alphaonegraphql.zip')
get_latest_artifact(bucket_path, module_py_path, '/var/temp/aws/alphaonepy.zip')








