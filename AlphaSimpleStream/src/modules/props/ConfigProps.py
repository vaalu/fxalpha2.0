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

AppProperties = {
	'COMMODITIES_MCX': json.loads(config.get('TRADING_INSTRUMENTS', 'instruments.commodities')),
	'ALPHAVANTAGE_KEY':config.get('TRADING_INSTRUMENTS', 'alphavantage.key'), 
	'ALPHAVANTAGE_URL':config.get('TRADING_INSTRUMENTS', 'alphavantage.url'), 
	'NIFTY50_URL':config.get('TRADING_INSTRUMENTS', 'nifty50.url'), 
	'KAFKA_URL':config.get('KAFKA', 'kafka.server.url'), 
	'KAFKA_PORT':config.get('KAFKA', 'kafka.server.port'), 
	'LOG_FILE':config.get('LOGGER', 'logging.file'),
	'LOG_OHLC_FILE':config.get('LOGGER', 'logging.ohlc.file'),
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

log_level_config = AppProperties['LOG_LEVEL']
default_log_level = log_level["info"]

if log_level_config != None:
	default_log_level = log_level[log_level_config.lower()]

logging.basicConfig( format='%(asctime)s : %(levelname)s : %(name)s : %(message)s', 
					level=default_log_level )
logging.log(logging.DEBUG, 'Starting logger')

app_logger = logging.getLogger('app_logger')
app_logger.setLevel(default_log_level)

rotating_handler = handlers.RotatingFileHandler(AppProperties['LOG_FILE'], maxBytes=50000000, backupCount=20)
app_logger.addHandler(rotating_handler)

# ohlc_rotating_handler = handlers.RotatingFileHandler(AppProperties['LOG_OHLC_FILE'], maxBytes=50000000, backupCount=20)
# app_logger.addHandler(ohlc_rotating_handler)

class AppOHLCLogger():
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
