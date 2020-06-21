from datetime import datetime
from dateutil import tz
import pytz
from modules.OHLCProcessor import OHLCProcessor
from modules.props.ConfigProps import AppProps, AppLogger
from modules.util.RedisUtil import RedisUtil
from modules.util.DateTimeUtil import DateTimeUtil

logger = AppLogger('EODProcessor')
class EODProcessor():
	__red_util = RedisUtil.get_instance()
	__red = RedisUtil.get_instance()
	__date_util = DateTimeUtil.get_instance()
	__offset = offset = datetime.now(pytz.timezone('Asia/Kolkata')).utcoffset().total_seconds()
	def __init__(self):
		logger.info('Starting EOD Process')
	def __get_local_date(self):
		return datetime.now().astimezone(tz.gettz('Asia/Kolkata'))
	def initialize_process(self, instruments):
		logger.info('Initializing one min process for the day')
		start_time, end_equities, end_commodities = self.__date_util.get_market_timings()
		all_instrument_ids = []
		for instrument in instruments:
			all_instrument_ids.append(instrument["token"])
		time_limit = 60 * 1
		init_time = start_time
		logger.info('Calculating 5 min ohlc data')
		while init_time < end_commodities:
			OHLCProcessor().process_all_from_cache_with_limit(all_instrument_ids,init_time,init_time+time_limit,1)
			init_time += time_limit
		init_time = start_time
		time_limit = 60 * 5
		while init_time < end_commodities:
			OHLCProcessor().process_all_from_cache_with_limit(all_instrument_ids,init_time,init_time+time_limit,5)
			init_time += time_limit

	def initialize_calculations(self):
		equities, commodities, all_instruments = self.__red.fetch_all_instruments()
		self.initialize_process(all_instruments)