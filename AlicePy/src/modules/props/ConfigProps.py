#!/usr/bin/env python3
import json
import configparser
import logging
import logging.handlers as handlers

print('Fetching access token from alice blue ant API')
config = configparser.ConfigParser()
config.read('application.config.properties')

# alphavantage.key=5U19TJGGJJNLYEIR
# alphavantage.url=https://www.alphavantage.co

aliceAnt = {
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
	'KAFKA_URL':config.get('KAFKA', 'kafka.server.url'), 
	'KAFKA_PORT':config.get('KAFKA', 'kafka.server.port'), 
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

log_level_config = aliceAnt['LOG_LEVEL']
default_log_level = log_level["info"]

if log_level_config != None:
	default_log_level = log_level[log_level_config.lower()]

logging.basicConfig( format='%(asctime)s : %(levelname)s : %(name)s : %(message)s', 
					level=default_log_level )
logging.log(logging.DEBUG, 'Starting logger')

app_logger = logging.getLogger('app_logger')
app_logger.setLevel(default_log_level)

rotating_handler = handlers.RotatingFileHandler(aliceAnt['LOG_FILE'], maxBytes=5000000, backupCount=200)
app_logger.addHandler(rotating_handler)

class AppLogger():
	def debug(self, msg):
		app_logger.debug(msg)
		if log_level_config.lower() == "console":
			print(msg)
	def error(self, msg):
		app_logger.error(msg)
		if log_level_config.lower() == "console":
			print(msg)
	def critical(self, msg):
		app_logger.critical(msg)
		if log_level_config.lower() == "console":
			print(msg)
	def fatal(self, msg):
		app_logger.fatal(msg)
		if log_level_config.lower() == "console":
			print(msg)
	def info(self, msg):
		app_logger.info(msg)
		if log_level_config.lower() == "console":
			print(msg)