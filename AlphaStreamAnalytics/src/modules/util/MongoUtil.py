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
	__db = __mongo['fxsource']
	def __init__(self):
		print('Initializing Mongo')
	def check_for_index(self, collection_name):
		index_names = ['date']
		for index_name in index_names:
			if index_name not in self.__db[collection_name].index_information():
				self.__db[collection_name].create_index(index_name, unique=True)

	def eod_save(self, collection, data):
		self.check_for_index(collection)
		coll = self.__db[collection]
		insert_ids = coll.insert_many(data)
		logger.info('Instruments for the day saved successfully')
