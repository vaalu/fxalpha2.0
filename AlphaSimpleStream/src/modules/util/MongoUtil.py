from modules.props.ConfigProps import AppProperties, AppLogger
from pymongo import MongoClient
import urllib

logger = AppLogger()

class MongoUtil():

	def __init__(self):
		print('Initializing Mongo')
		user = AppProperties['MONGO_USER']
		passw = urllib.parse.quote_plus(AppProperties['MONGO_PASSWORD'])
		mongo_server='%s:%s'%(AppProperties['MONGO_URL'], AppProperties['MONGO_PORT'])
		mongo_uri = 'mongodb://%s:%s@%s/'%(user, passw, mongo_server)
		client = MongoClient(mongo_uri)
		logger.info(client.list_database_names())
