#!/usr/bin/env python
import configparser
import boto3
import botocore
import pytz
import os
import json
import shutil
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
module_stream_path = config.get('DEPLOYMENT', 'deploy.artifact.s3.path.stream')
module_analytics_path = config.get('DEPLOYMENT', 'deploy.artifact.s3.path.analytics')

deploy_location = config.get('DEPLOYMENT', 'deploy.artifact.local.path')

security_server = config.get('SECURITY', 'deploy.security.server')
security_realm = config.get('SECURITY', 'deploy.security.realm')

alice_clientid = config.get('ALICE', 'deploy.alice.clientid')
alice_user = config.get('ALICE', 'deploy.alice.user')
alice_client_secret = config.get('ALICE', 'deploy.alice.client.secret')
alice_client_password = config.get('ALICE', 'deploy.alice.client.password')
alphavantage_key =  config.get('ALICE', 'deploy.alphavantage.key')

kafka_url=config.get('KAFKA', 'deploy.kafka.server.url')
kafka_port=config.get('KAFKA', 'deploy.kafka.server.port')

log_dir=config.get('LOGGER', 'deploy.logging.dir')
log_file=config.get('LOGGER', 'deploy.logging.file')
log_level=config.get('LOGGER', 'deploy.logging.level')

mongo_url=config.get('MONGO', 'deploy.mongo.server.url')
mongo_port=config.get('MONGO', 'deploy.mongo.server.port')
mongo_user=config.get('MONGO', 'deploy.mongo.server.user')
mongo_password=config.get('MONGO', 'deploy.mongo.server.password')

telebot_token=config.get('TELEBOT', 'deploy.telegram.bot.token')
telebot_chat_id=config.get('TELEBOT', 'deploy.telegram.bot.chatid')

client = boto3.client(
    's3',
    aws_access_key_id=accessKey,
    aws_secret_access_key=secretKey
)
response = client.list_buckets()

def get_latest_artifact(bucket, prefix, saving_file_name):
	uiartifacts = client.list_objects(Bucket=bucket, Prefix=prefix)
	uiartifact_contents = uiartifacts['Contents']
	latest_artifact = sorted(uiartifact_contents, key=lambda x: x['LastModified'], reverse=True)[0]
	client.download_file(bucket, latest_artifact['Key'], saving_file_name)

def prepare_download_path(download_loc):
	return (deploy_location if deploy_location.endswith('/') else deploy_location + '/') + (download_loc if download_loc != '/' else '')

loc = prepare_download_path('/')
print ('Download location: %s'%(loc))
try:
	# print('Removing existing directory')
	# shutil.rmtree(loc)
	print('Creating new directory')
	os.makedirs(loc)
except OSError as e:
	print ('Directory already present (or) Error while creating directory')

localpath_ui=prepare_download_path('alphaoneui.zip')
localpath_graphql=prepare_download_path('alphaonegraphql.zip')
localpath_py=prepare_download_path('alphaonepy.zip')
localpath_stream=prepare_download_path('alphastream.zip')
localpath_analytics=prepare_download_path('alphastreamanalytics.zip')

def prepare_artifacts_ui():
	print ('Downloading artifacts: alphaoneui %s'%(datetime.now()))
	get_latest_artifact(bucket_path, module_ui_path, localpath_ui)
	print ('Downloading artifacts: ended %s'%(datetime.now()))
def prepare_artifacts_graphql():
	print ('Downloading artifacts: alphaonegraphql %s'%(datetime.now()))
	get_latest_artifact(bucket_path, module_graphql_path, localpath_graphql)
	print ('Downloading artifacts: ended %s'%(datetime.now()))
def prepare_artifacts_py():	
	print ('Downloading artifacts: alphaonepy %s'%(datetime.now()))
	get_latest_artifact(bucket_path, module_py_path, localpath_py)
	print ('Downloading artifacts: ended %s'%(datetime.now()))
def prepare_artifacts_stream():
	print ('Downloading artifacts: alphaonepy %s'%(datetime.now()))
	get_latest_artifact(bucket_path, module_stream_path, localpath_stream)
	print ('Downloading artifacts: ended %s'%(datetime.now()))
def prepare_artifacts_analytics():
	print ('Downloading artifacts: alpha-analytics %s'%(datetime.now()))
	get_latest_artifact(bucket_path, module_analytics_path, localpath_analytics)
	print ('Downloading artifacts: ended %s'%(datetime.now()))

def extract_artifacts_ui():
	print ('Extracting artifacts: alphaoneui: %s'%(datetime.now()))
	with ZipFile(localpath_ui) as zipObj:
		zipObj.extractall(loc)
def extract_artifacts_graphql():
	print ('Extracting artifacts: alphaonegraphql: %s'%(datetime.now()))
	with ZipFile(localpath_graphql) as zipObj:
		zipObj.extractall(loc)
def extract_artifacts_py():
	print ('Extracting artifacts: alphaonepy: %s'%(datetime.now()))
	with ZipFile(localpath_py) as zipObj:
		zipObj.extractall(loc)
	print ('Extracting artifacts: ended: %s'%(datetime.now()))
def extract_artifacts_stream():
	print ('Extracting artifacts: alphaonepy: %s'%(datetime.now()))
	with ZipFile(localpath_stream) as zipObj:
		zipObj.extractall(loc)
	print ('Extracting artifacts: ended: %s'%(datetime.now()))
def extract_artifacts_analytics():
	print ('Extracting artifacts: alphastream-analytics: %s'%(datetime.now()))
	with ZipFile(localpath_analytics) as zipObj:
		zipObj.extractall(loc)
	print ('Extracting artifacts: ended: %s'%(datetime.now()))
def update_properties_ui():
	print ('Updating the properties: %s'%(datetime.now()))
	keycloak_json_file = loc + 'alphaoneui/build/keycloak.json'
	print ('JSON File location: %s'%(keycloak_json_file))

	keycloak_json = {}
	with open(keycloak_json_file, 'r+') as keycloak_file:
		keycloak_json = json.load(keycloak_file)
		keycloak_json['realm']=security_realm
		keycloak_json['auth-server-url']=security_server
		keycloak_file.close()
	print (keycloak_json)
	with open(keycloak_json_file, 'w+') as keycloak_file:
		json.dump(keycloak_json, keycloak_file)
		keycloak_file.close()
	print ('Completed updating properties: %s'%(datetime.now()))
	
def update_properties_py():
	alice_props = loc + 'AlicePy/application.config.properties'
	alice_config = configparser.ConfigParser()
	alice_config.read(alice_props)
	
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.id', alice_clientid)
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.user', alice_user)
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.secret', alice_client_secret)
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.password', alice_client_password)
	alice_config.set('TRADING_INSTRUMENTS', 'alphavantage.key', alphavantage_key)
	alice_config.set('KAFKA', 'kafka.server.url', kafka_url)
	alice_config.set('KAFKA', 'kafka.server.port', kafka_port)
	alice_config.set('LOGGER', 'logging.file', log_file)
	alice_config.set('LOGGER', 'logging.level', log_level)

	with open(alice_props, 'w+') as alice_file:
		alice_config.write(alice_file)
		alice_file.close()

def update_properties_alphastream():
	print ('Updating alpha stream properties: %s'%(datetime.now()))
	
	alpha_props = loc + 'AlphaSimpleStream/application.config.properties'
	alice_config = configparser.ConfigParser()
	alice_config.read(alpha_props)
	
	alice_config.set('TRADING_INSTRUMENTS', 'alphavantage.key', alphavantage_key)
	alice_config.set('MONGO', 'mongo.password', mongo_password)
	alice_config.set('KAFKA', 'kafka.server.url', kafka_url)
	alice_config.set('KAFKA', 'kafka.server.port', kafka_port)
	alice_config.set('LOGGER', 'logging.file', log_file)
	alice_config.set('LOGGER', 'logging.level', log_level)
	alice_config.set('MONGO', 'mongo.server.url', mongo_url)
	alice_config.set('MONGO', 'mongo.server.port', mongo_port)
	alice_config.set('MONGO', 'mongo.user', mongo_user)
	alice_config.set('MONGO', 'mongo.password', mongo_password)
	
	with open(alpha_props, 'w+') as alice_file:
		alice_config.write(alice_file)
		alice_file.close()

def update_properties_alpha_analytics():
	print ('Updating alpha analytics properties: %s'%(datetime.now()))
	
	alpha_props = loc + 'AlphaStreamAnalytics/application.config.properties'
	alice_config = configparser.ConfigParser()
	alice_config.read(alpha_props)
	
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.id', alice_clientid)
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.user', alice_user)
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.secret', alice_client_secret)
	alice_config.set('ALICE_ANT_OAUTH2', 'alice.ant.client.password', alice_client_password)
	alice_config.set('TRADING_INSTRUMENTS', 'alphavantage.key', alphavantage_key)
	alice_config.set('TRADING_INSTRUMENTS', 'telegram.bot.token', telebot_token)
	alice_config.set('TRADING_INSTRUMENTS', 'telegram.bot.chatid', telebot_chat_id)
	alice_config.set('LOGGER', 'logging.dir', log_dir)
	alice_config.set('LOGGER', 'logging.file', log_file)
	alice_config.set('LOGGER', 'logging.level', log_level)
	alice_config.set('MONGO', 'mongo.server.url', mongo_url)
	alice_config.set('MONGO', 'mongo.server.port', mongo_port)
	alice_config.set('MONGO', 'mongo.user', mongo_user)
	alice_config.set('MONGO', 'mongo.password', mongo_password)
	
	with open(alpha_props, 'w+') as alice_file:
		alice_config.write(alice_file)
		alice_file.close()

def prepare_artifacts():
	print ('Preparing artifacts: %s'%(datetime.now()))
	# prepare_artifacts_ui()
	# prepare_artifacts_graphql()
	# prepare_artifacts_py()
	# prepare_artifacts_stream()
	prepare_artifacts_analytics()

def extract_artifacts():
	print ('Extracting artifacts: in appropriate locations %s'%(datetime.now()))
	# extract_artifacts_ui()
	# extract_artifacts_graphql()
	# extract_artifacts_py()
	# extract_artifacts_stream()
	extract_artifacts_analytics()

def update_properties():
	print ('Updating properties: in appropriate locations %s'%(datetime.now()))
	# update_properties_ui()
	# update_properties_py()
	# update_properties_alphastream()
	update_properties_alpha_analytics()

prepare_artifacts()
extract_artifacts()
update_properties()




