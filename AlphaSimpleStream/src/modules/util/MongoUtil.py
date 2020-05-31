from modules.props.ConfigProps import AppProperties, AppLogger
from pymongo import MongoClient
import urllib

logger = AppLogger()

class MongoUtil():

	user = AppProperties['MONGO_USER']
	passw = urllib.parse.quote_plus(AppProperties['MONGO_PASSWORD'])
	mongo_server='%s:%s'%(AppProperties['MONGO_URL'], AppProperties['MONGO_PORT'])
	mongo_uri = 'mongodb://%s:%s@%s/'%(user, passw, mongo_server)
	__mongo = MongoClient(mongo_uri)
	def __init__(self):
		print('Initializing Mongo')
		self.__mongo['fxsource']
	def eod_save(self, instrument_name, data):
		logger.info('Saving for instrument %s'%instrument_name)
		logger.info(data)
