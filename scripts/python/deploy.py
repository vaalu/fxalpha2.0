#!/usr/bin/env python
import configparser
import boto3
import botocore
from datetime import datetime
import pytz
import os
from zipfile import ZipFile

config = configparser.ConfigParser()
config.read('aws.config.properties')

accessKey = config.get('AWS', 'aws.access.key')
secretKey = config.get('AWS', 'aws.secret.key')
bucket_path = config.get('DEPLOYMENT', 'deploy.artifact.s3.path.bucket')
module_ui_path = config.get('DEPLOYMENT', 'deploy.artifact.s3.path.ui')
module_graphql_path = config.get('DEPLOYMENT', 'deploy.artifact.s3.path.graphql')
module_py_path = config.get('DEPLOYMENT', 'deploy.artifact.s3.path.py')
deploy_location = config.get('DEPLOYMENT', 'deploy.artifact.local.path')

client = boto3.client(
    's3',
    aws_access_key_id=accessKey,
    aws_secret_access_key=secretKey
)
response = client.list_buckets()

# for bucket in response['Buckets']:
# 	print bucket["Name"]

def get_latest_artifact(bucket, prefix, saving_file_name):
	uiartifacts = client.list_objects(Bucket=bucket, Prefix=prefix)
	uiartifact_contents = uiartifacts['Contents']
	latest_artifact = sorted(uiartifact_contents, key=lambda x: x['LastModified'], reverse=True)[0]
	# print 'Latest build artifact: %s'%(latest_artifact['Key'])
	client.download_file(bucket, latest_artifact['Key'], saving_file_name)

def prepare_download_path(download_loc):
	return (deploy_location if deploy_location.endswith('/') else deploy_location + '/') + (download_loc if download_loc != '/' else '')

loc = prepare_download_path('/')
print 'Download location: %s'%(loc)
try:
	os.makedirs(loc)
except OSError as e:
	print 'Directory already present (or) Error while creating directory'

localpath_ui=prepare_download_path('alphaoneui.zip')
localpath_graphql=prepare_download_path('alphaonegraphql.zip')
localpath_py=prepare_download_path('alphaonepy.zip')

def prepare_artifacts():
	print 'Downloading artifacts: alphaoneui %s'%(datetime.now())
	get_latest_artifact(bucket_path, module_ui_path, localpath_ui)

	print 'Downloading artifacts: alphaonegraphql %s'%(datetime.now())
	get_latest_artifact(bucket_path, module_graphql_path, localpath_graphql)
	
	print 'Downloading artifacts: alphaonepy %s'%(datetime.now())
	get_latest_artifact(bucket_path, module_py_path, localpath_py)
	print 'Downloading artifacts ended %s'%(datetime.now())

def extract_artifacts():
	print 'Extracting artifacts in appropriate locations %s'%(datetime.now())
	print 'Extracting artifacts: alphaoneui: %s'%(datetime.now())
	with ZipFile(localpath_ui) as zipObj:
		zipObj.extractall(loc)
	print 'Extracting artifacts: alphaonegraphql: %s'%(datetime.now())
	with ZipFile(localpath_graphql) as zipObj:
		zipObj.extractall(loc)
	print 'Extracting artifacts: alphaonepy: %s'%(datetime.now())
	with ZipFile(localpath_py) as zipObj:
		zipObj.extractall(loc)
	print 'Extracting artifacts: ended: %s'%(datetime.now())

prepare_artifacts()
extract_artifacts()






