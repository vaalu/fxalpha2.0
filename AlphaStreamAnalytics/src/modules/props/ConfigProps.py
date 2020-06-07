#!/usr/bin/env python3
import json
import configparser
import logging
import logging.handlers as handlers
import urllib

print('Fetching access token from alice blue ant API')
config = configparser.ConfigParser()
config.read('application.config.properties')

AppProps = {
	'CLIENT_ID' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.id'), 
	'CLIENT_USER' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.user'), 
	'CLIENT_SECRET' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.secret'), 
	'CLIENT_PASSWORD' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.password'), 
	'URL_AUTH' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.auth'), 
	'URL_TOKEN' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.token'), 
	'URL_CALLBACK' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.callback'), 
	'URL_LOGIN' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.login'),
	'URL_2FA' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.2fa'),
	'URL_WSS' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.wss'), 
	'ALICE_API_BASE': config.get('ALICE_ANT_API', 'alice.ant.api.base'),
	'ALICE_PROFILE' : config.get('ALICE_ANT_API', 'alice.ant.api.profile'),
	'COMMODITIES_MCX': json.loads(config.get('TRADING_INSTRUMENTS', 'instruments.commodities')),
	'LEGACY_COMMODITIES':json.loads(config.get('TRADING_INSTRUMENTS', 'legacy.instruments.commodities')), 
	'ALPHAVANTAGE_KEY':config.get('TRADING_INSTRUMENTS', 'alphavantage.key'), 
	'ALPHAVANTAGE_URL':config.get('TRADING_INSTRUMENTS', 'alphavantage.url'), 
	'NIFTY50_URL':config.get('TRADING_INSTRUMENTS', 'nifty50.url'), 
	'MONGO_URL':config.get('MONGO', 'mongo.server.url'), 
	'MONGO_PORT':config.get('MONGO', 'mongo.server.port'), 
	'MONGO_USER':config.get('MONGO', 'mongo.user'), 
	'MONGO_PASSWORD':config.get('MONGO', 'mongo.password'), 
	'LOG_FILE':config.get('LOGGER', 'logging.file'),
	'LOG_LEVEL':config.get('LOGGER', 'logging.level')
}

log_level = {
	"info":logging.INFO, 
	"error":logging.ERROR, 
	"debug":logging.DEBUG, 
	"critical":logging.CRITICAL, 
	"fatal":logging.FATAL, 
	"console":logging.INFO
}

log_level_config = AppProps['LOG_LEVEL']
default_log_level = log_level["info"]

if log_level_config != None:
	default_log_level = log_level[log_level_config.lower()]
# logging.basicConfig( format='%(asctime)s : %(levelname)s : %(name)s : %(message)s', level=default_log_level )
log_format = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
logging.basicConfig( format='%(asctime)s : %(levelname)s : %(message)s', level=default_log_level )
rotating_handler = handlers.RotatingFileHandler(AppProps['LOG_FILE'], maxBytes=5000000, backupCount=200)
rotating_handler.setFormatter(log_format)
app_logger = logging.getLogger('alpha_analytics')
app_logger.addHandler(rotating_handler)
app_logger.setLevel(default_log_level)
logging.log(logging.DEBUG, 'Starting logger')

def rerun_curl():
	app_logger.info('Connection is closed. Hence reopening it again')
	urllib.request.urlopen('http://localhost:5000/')

class AppLogger():
	__name=''
	def __init__(self, name):
		self.__name = name
	def debug(self, msg):
		app_logger.debug('%s : %s'%(self.__name, msg))
		if log_level_config.lower() == "console":
			print('%s : %s'%(self.__name, msg))
	def error(self, msg):
		app_logger.error('%s : %s'%(self.__name, msg))
		rerun_curl()
		if log_level_config.lower() == "console":
			print('%s : %s'%(self.__name, msg))
	def critical(self, msg):
		app_logger.critical('%s : %s'%(self.__name, msg))
		if log_level_config.lower() == "console":
			print('%s : %s'%(self.__name, msg))
	def fatal(self, msg):
		app_logger.fatal('%s : %s'%(self.__name, msg))
		if log_level_config.lower() == "console":
			print('%s : %s'%(self.__name, msg))
	def info(self, msg):
		app_logger.info('%s : %s'%(self.__name, msg))
		if log_level_config.lower() == "console":
			print('%s : %s'%(self.__name, msg))