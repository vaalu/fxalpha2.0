from datetime import datetime
from dateutil import tz
import pytz
from modules.props.ConfigProps import AppProps, AppLogger
from modules.util.RedisUtil import RedisUtil
from modules.util.MongoUtil import MongoUtil

logger = AppLogger('EODProcessor')
class EODProcessor():
	__red_util = RedisUtil()
	__mongo = MongoUtil()
	def __init__(self):
		logger.info('Starting EOD Process')
	def __get_local_date(self):
		return datetime.now().astimezone(tz.gettz('Asia/Kolkata'))
	def initialize_1_min_process_with_instr(self, instruments):
		logger.info('Initializing one min process for the day')
	def initialize_1_min_process(self):
		logger.info('Initializing one min process for the day')
		equities = self.__red_util.fetch_processing_instruments('EQUITY')
		commodities = self.__red_util.fetch_processing_instruments('COMMODITY')
		all_instruments = list([])
		for instrument in equities:
			all_instruments.append({
				'instrument':instrument["token"],
				'type':'EQUITY', 
				'detail':instrument
			})
		for instrument in commodities:
			all_instruments.append({
				'instrument':instrument["token"],
				'type':'COMMODITY', 
				'detail':instrument
			})
		current_date = str(self.__get_local_date().strftime('%Y-%m-%d'))
		instr_data = {
			"date":current_date,
			"instruments":all_instruments
		}
		self.__mongo.eod_save('DailyData', [instr_data])
		self.initialize_1_min_process_with_instr(all_instruments)