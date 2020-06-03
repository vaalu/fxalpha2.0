from modules.props.ConfigProps import AppProps, AppLogger
from modules.util.RedisUtil import RedisUtil
from modules.util.MongoUtil import MongoUtil

logger = AppLogger('EODProcessor')
class EODProcessor():
	__red_util = RedisUtil()
	__mongo = MongoUtil()
	def __init__(self):
		logger.info('Starting EOD Process')
	def initialize_1_min_process(self):
		logger.info('Initializing one min process for the day')
	def initialize_1_min_process_with_instr(self, instruments):
		logger.info('Initializing one min process for the day')
		
