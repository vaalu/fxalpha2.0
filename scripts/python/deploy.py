#!/usr/bin/env python
import configparser
import boto3
import botocore
import pytz
import os
import json
from datetime import datetime
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

security_server = config.get('SECURITY', 'deploy.security.server')
security_realm = config.get('SECURITY', 'deploy.security.realm')

alice_clientid = config.get('ALICE', 'deploy.alice.clientid')
alice_user = config.get('ALICE', 'deploy.alice.user')
alice_client_secret = config.get('ALICE', 'deploy.alice.client.secret')
alice_client_password = config.get('ALICE', 'deploy.alice.client.password')


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
	print 'Downloading artifacts: ended %s'%(datetime.now())

def extract_artifacts():
	print 'Extracting artifacts: in appropriate locations %s'%(datetime.now())
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

def update_properties():
	print 'Updating the properties: %s'%(datetime.now())
	keycloak_json_file = loc + 'alphaoneui/build/keycloak.json'
	print 'JSON File location: %s'%(keycloak_json_file)

	keycloak_json = {}
	with open(keycloak_json_file, 'r+') as keycloak_file:
		keycloak_json = json.load(keycloak_file)
		keycloak_json['realm']=security_realm
		keycloak_json['auth-server-url']=security_server
		keycloak_file.close()
	print keycloak_json
	with open(keycloak_json_file, 'w+') as keycloak_file:
		json.dump(keycloak_json, keycloak_file)
		keycloak_file.close()
	print 'Completed updating properties: %s'%(datetime.now())
	alice_props = loc + 'AlicePy/application.config.properties'
	alice_config = configparser.ConfigParser()
	alice_config.read(alice_props)
	
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.id', alice_clientid)
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.user', alice_user)
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.secret', alice_client_secret)
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.password', alice_client_password)
	
	with open(alice_props, 'w+') as alice_file:
		alice_config.write(alice_file)
		alice_file.close()

prepare_artifacts()
extract_artifacts()
update_properties()





