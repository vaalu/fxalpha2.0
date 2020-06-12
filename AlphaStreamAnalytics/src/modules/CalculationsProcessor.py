import pytz
from datetime import datetime
from dateutil import tz
from modules.props.ConfigProps import AppLogger, AppProps
from modules.util.CalculationsUtil import CalculationsUtil
from modules.util.DateTimeUtil import DateTimeUtil
from modules.util.RedisUtil import RedisUtil

logger = AppLogger('CalculationsProcessor')

class CalculationsProcessor():
	__calculations_util = None
	__dateutil = None
	__red_util = None
	def __init__(self, dateutil):
		logger.info('Starting calculations')
		self.__dateutil = DateTimeUtil()
		self.__calculations_util = CalculationsUtil(self.__dateutil)
		self.__red_util = RedisUtil()
	def __process(self):
		logger.info('Processing started')
	def get_instruments(self):
		equities = self.__red_util.fetch_processing_instruments('EQUITY')
		commodities = self.__red_util.fetch_processing_instruments('COMMODITY')
		all_instruments = list([])
		all_instruments.extend(equities)
		all_instruments.extend(commodities)
		return equities, commodities, all_instruments
	def process_calculations(self):
		# start_time, end_time_equities, end_time_commodities = self.__dateutil.get_market_timings_previous_day() 
		# start_time, end_time_equities, end_time_commodities = self.__dateutil.get_market_timings()
		start_time = 1591761180
		process_init_1 = start_time
		duration = 60
		equities, commodities, all_instruments = self.get_instruments()
		# logger.info('Process starts by %i : equities end %i commodities end %i'%(start_time, end_time_equities, end_time_commodities))
		instrument = '219484'
		while process_init_1 < (start_time + duration * 120):
			# keys_time = [('%s:1M:%s'%(instrument["token"],int(process_init_1 - (duration*index))) if (process_init_1 - (duration*index)) > start_time else '%s:1M:%i'%(instrument["token"],start_time)) for index in range(0, 40)]
			# keys_time = [('%s:1M:%s'%(instrument["token"],int(process_init_1 - (duration*index))) if (process_init_1 - (duration*index)) > start_time else '%s:1M:%i'%(instrument["token"],int(start_time))) for index in range(0, 40)]
			keys_time = ['%s:1M:%i'%(instrument, (process_init_1 - (duration*index)))for index in range(0, 40)]
			# logger.info('Series to be calculated: %s'%str(keys_time))
			self.__calculations_util.calculate_1_min(instrument, keys_time)
			process_init_1 += duration
			# process_init_1 = process_init_1 + duration










