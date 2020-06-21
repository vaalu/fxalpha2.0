#!/usr/bin/env python3
import json
import configparser
import logging
import logging.handlers as handlers
import urllib
try:
	import thread
except ImportError:
	import _thread as thread
import time

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
	'KITE_API_KEY' : config.get('KTIE_API', 'kite.api.key'),
	'KITE_API_SECRET' : config.get('KITE_API', 'ktie.api.secret'),
	'TIME_ZONE' : config.get('DATE_TIME', 'time.zone'),
	'COMMODITIES_MCX': json.loads(config.get('TRADING_INSTRUMENTS', 'instruments.commodities')),
	'LEGACY_COMMODITIES':json.loads(config.get('TRADING_INSTRUMENTS', 'legacy.instruments.commodities')), 
	'ALPHAVANTAGE_KEY':config.get('TRADING_INSTRUMENTS', 'alphavantage.key'), 
	'ALPHAVANTAGE_URL':config.get('TRADING_INSTRUMENTS', 'alphavantage.url'), 
	'NIFTY50_URL':config.get('TRADING_INSTRUMENTS', 'nifty50.url'), 
	'MONGO_URL':config.get('MONGO', 'mongo.server.url'), 
	'MONGO_PORT':config.get('MONGO', 'mongo.server.port'), 
	'MONGO_USER':config.get('MONGO', 'mongo.user'), 
	'MONGO_PASSWORD':config.get('MONGO', 'mongo.password'), 
	'LOG_DIR':config.get('LOGGER', 'logging.dir'),
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
log_format = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
logging.basicConfig( format='%(asctime)s : %(levelname)s : %(name)s : %(message)s', level=default_log_level )
rotating_handler = handlers.RotatingFileHandler(AppProps['LOG_FILE'], maxBytes=5000000, backupCount=200)
rotating_handler.setFormatter(log_format)
app_logger = logging.getLogger('alpha_analytics')
app_logger.addHandler(rotating_handler)
app_logger.setLevel(default_log_level)
logging.log(logging.DEBUG, 'Starting logger')

def setup_logger(name, log_file, level=logging.INFO):
	# local_handler = logging.FileHandler(log_file)
	local_handler = handlers.RotatingFileHandler(log_file, maxBytes=5000000, backupCount=200)
	local_handler.setFormatter(log_format)
	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.addHandler(local_handler)
	return logger

logger_file = '%s-ohlc.log'%(AppProps['LOG_FILE'])
logger_ohlc = setup_logger('alpha_ohlc', logger_file, default_log_level)

logger_redis_file = '%s-cache.log'%(AppProps['LOG_FILE'])
logger_redis = setup_logger('alpha_redis', logger_redis_file, default_log_level)

logger_calc_file = '%s-calc.log'%(AppProps['LOG_FILE'])
logger_calc = setup_logger('alpha_calc', logger_calc_file, default_log_level)

logger_stream_file = '%s-stream.log'%(AppProps['LOG_FILE'])
logger_stream = setup_logger('alpha_stream', logger_stream_file, default_log_level)

logger_backup_file = '%s-data-bkp.log'%(AppProps['LOG_FILE'])
logger_backup = setup_logger('backup', logger_backup_file, default_log_level)

logger_kite_file = '%s-kite.log'%(AppProps['LOG_FILE'])
logger_kite = setup_logger('kite', logger_kite_file, default_log_level)

def rerun_curl():
	time.sleep(10)
	app_logger.info('Connection is closed. Hence reopening it again')
	urllib.request.urlopen('http://localhost:5000/')

class AppLogger():
	__name=''
	__logger = app_logger
	def __init__(self, name):
		self.__name = name
	def debug(self, msg):
		self.__logger.debug('%s : %s'%(self.__name, msg))
	def error(self, msg):
		self.__logger.error('%s : %s'%(self.__name, msg))
		if '...Feed data socket closed...' in msg or 'Websocket Error' in msg:
			rerun_curl()
	def critical(self, msg):
		self.__logger.critical('%s : %s'%(self.__name, msg))
	def fatal(self, msg):
		self.__logger.fatal('%s : %s'%(self.__name, msg))
	def info(self, msg):
		self.__logger.info('%s : %s'%(self.__name, msg))

class AppOHLCLogger():
	__name=''
	__logger = logger_ohlc
	def __init__(self, name):
		self.__name = name
	def debug(self, msg):
		self.__logger.debug('%s : %s'%(self.__name, msg))
	def error(self, msg):
		self.__logger.error('%s : %s'%(self.__name, msg))
	def critical(self, msg):
		self.__logger.critical('%s : %s'%(self.__name, msg))
	def fatal(self, msg):
		self.__logger.fatal('%s : %s'%(self.__name, msg))
	def info(self, msg):
		self.__logger.info('%s : %s'%(self.__name, msg))

class AppCacheLogger():
	__name=''
	__logger = logger_redis
	def __init__(self, name):
		self.__name = name
	def debug(self, msg):
		self.__logger.debug('%s : %s'%(self.__name, msg))
	def error(self, msg):
		self.__logger.error('%s : %s'%(self.__name, msg))
	def critical(self, msg):
		self.__logger.critical('%s : %s'%(self.__name, msg))
	def fatal(self, msg):
		self.__logger.fatal('%s : %s'%(self.__name, msg))
	def info(self, msg):
		self.__logger.info('%s : %s'%(self.__name, msg))

class AppCalcLogger():
	__name=''
	__logger = logger_calc
	def __init__(self, name):
		self.__name = name
	def debug(self, msg):
		self.__logger.debug('%s : %s'%(self.__name, msg))
	def error(self, msg):
		self.__logger.error('%s : %s'%(self.__name, msg))
	def critical(self, msg):
		self.__logger.critical('%s : %s'%(self.__name, msg))
	def fatal(self, msg):
		self.__logger.fatal('%s : %s'%(self.__name, msg))
	def info(self, msg):
		self.__logger.info('%s : %s'%(self.__name, msg))


class AppStreamLogger():
	__name='DefaultMessageHandler'
	__logger = logger_stream
	__instance = None
	@staticmethod
	def get_instance():
		if AppStreamLogger.__instance == None:
			AppStreamLogger()
		return AppStreamLogger.__instance
	def __init__(self):
		if AppStreamLogger.__instance != None:
			raise Exception('AppStreamLogger is now singleton')
		else:
			AppStreamLogger.__instance = self
	def debug(self, msg):
		self.__logger.debug('%s : %s'%(self.__name, msg))
	def error(self, msg):
		self.__logger.error('%s : %s'%(self.__name, msg))
	def critical(self, msg):
		self.__logger.critical('%s : %s'%(self.__name, msg))
	def fatal(self, msg):
		self.__logger.fatal('%s : %s'%(self.__name, msg))
	def info(self, msg):
		self.__logger.info('%s : %s'%(self.__name, msg))

AppStreamLogger()

class AppDataBackupLogger():
	__name='AppDataBackupLogger'
	__logger = logger_backup
	__instance = None
	@staticmethod
	def get_instance():
		if AppDataBackupLogger.__instance == None:
			AppDataBackupLogger()
		return AppDataBackupLogger.__instance
	def __init__(self):
		if AppDataBackupLogger.__instance != None:
			raise Exception('AppDataBackupLogger is now singleton')
		else:
			AppDataBackupLogger.__instance = self
	def debug(self, msg):
		self.__logger.debug('%s : %s'%(self.__name, msg))
	def error(self, msg):
		self.__logger.error('%s : %s'%(self.__name, msg))
	def critical(self, msg):
		self.__logger.critical('%s : %s'%(self.__name, msg))
	def fatal(self, msg):
		self.__logger.fatal('%s : %s'%(self.__name, msg))
	def info(self, msg):
		self.__logger.info('%s : %s'%(self.__name, msg))

AppDataBackupLogger()


class AppKiteLogger():
	__name='AppKiteLogger'
	__logger = logger_kite
	__instance = None
	@staticmethod
	def get_instance():
		if AppKiteLogger.__instance == None:
			AppKiteLogger()
		return AppKiteLogger.__instance
	def __init__(self):
		if AppKiteLogger.__instance != None:
			raise Exception('AppKiteLogger is now singleton')
		else:
			AppKiteLogger.__instance = self
	def debug(self, msg):
		self.__logger.debug('%s : %s'%(self.__name, msg))
	def error(self, msg):
		self.__logger.error('%s : %s'%(self.__name, msg))
	def critical(self, msg):
		self.__logger.critical('%s : %s'%(self.__name, msg))
	def fatal(self, msg):
		self.__logger.fatal('%s : %s'%(self.__name, msg))
	def info(self, msg):
		self.__logger.info('%s : %s'%(self.__name, msg))

AppKiteLogger()