from modules.props.ConfigProps import AppProps, AppLogger
from pymongo import MongoClient
import urllib

logger = AppLogger('MongoUtil')

class MongoUtil():

	user = AppProps['MONGO_USER']
	passw = urllib.parse.quote_plus(AppProps['MONGO_PASSWORD'])
	mongo_server='%s:%s'%(AppProps['MONGO_URL'], AppProps['MONGO_PORT'])
	mongo_uri = 'mongodb://%s:%s@%s/'%(user, passw, mongo_server)
	__mongo = MongoClient(mongo_uri)
	def __init__(self):
		print('Initializing Mongo')
		self.__mongo['fxsource']
	def eod_save(self, instrument_name, data):
		logger.info('Saving for instrument %s'%instrument_name)
		logger.info(data)
