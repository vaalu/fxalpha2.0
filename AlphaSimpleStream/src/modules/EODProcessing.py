from modules.props.ConfigProps import AppProperties, AppLogger
from modules.util.RedisUtil import RedisUtil
from modules.util.KafkaUtil import KafkaUtil
from modules.util.MongoUtil import MongoUtil

logger = AppLogger()
class EODProcessor():
	__red_util = RedisUtil()
	__mongo = MongoUtil()
	def __init__(self):
		logger.info('Starting EOD Process')
	def initialize_1_min_process(self):
		logger.info('Initializing one min process for the day')
	def initialize_1_min_process(self, instruments):
		logger.info('Initializing one min process for the day')
		
