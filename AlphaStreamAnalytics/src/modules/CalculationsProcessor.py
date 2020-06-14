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
	__dateutil = DateTimeUtil.get_instance()
	__red_util = RedisUtil.get_instance()
	__start_time, __end_time_equities, __end_time_commodities = __dateutil.get_market_timings()
	__equities = __red_util.fetch_processing_instruments('EQUITY')
	__commodities = __red_util.fetch_processing_instruments('COMMODITY')
	__all_instruments = list([])
	__all_instruments.extend(__equities)
	__all_instruments.extend(__commodities)
	__instance = None
	@staticmethod
	def get_instance():
		if CalculationsProcessor.__instance == None:
			CalculationsProcessor()
		return CalculationsProcessor.__instance
	def __init__(self):
		if CalculationsProcessor.__instance != None:
			raise Exception('DateTime util is now singleton')
		else:
			CalculationsProcessor.__instance = self
		logger.info('Starting calculations')
		self.__calculations_util = CalculationsUtil(self.__dateutil)
	def __process(self):
		logger.info('Processing started')
	def get_instruments(self):
		return self.__equities, self.__commodities, self.__all_instruments
	def process_calculations(self):
		process_init_1 = self.__start_time
		duration = 60
		equities, commodities, all_instruments = self.get_instruments()
		logger.info('Process starts by %i : equities end %i commodities end %i'%(self.__start_time, self.__end_time_equities, self.__end_time_commodities))
		# instrument = '219484'
		while process_init_1 < self.__end_time_commodities:
			for instr in all_instruments:
				instrument = instr["token"]
				keys_time = ['%s:1M:%i'%(instrument, (process_init_1 - (duration*index)))for index in range(0, 40)]
				self.__calculations_util.calculate_1_min(instrument, keys_time)
			process_init_1 += duration
	def process_1_min_calc(self, calc_start):
		duration = 60
		for instr in self.__all_instruments:
			instrument = instr["token"]
			keys_time = ['%s:1M:%i'%(instrument, (calc_start - (duration*index)))for index in range(0, 40)]
			self.__calculations_util.calculate_1_min(instrument, keys_time)
CalculationsProcessor()









