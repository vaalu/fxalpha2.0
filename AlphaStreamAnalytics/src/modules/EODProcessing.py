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
		processing_instruments = self.__red_util.fetch_processing_instruments('EQUITY')
		all_instruments = list([])
		for instrument in processing_instruments:
			all_instruments.append({
				'instrument':instrument["token"], 
				'detail':instrument
			})
		self.__mongo.eod_save('EQUITIES', all_instruments)
	def initialize_1_min_process_with_instr(self, instruments):
		logger.info('Initializing one min process for the day')
		
