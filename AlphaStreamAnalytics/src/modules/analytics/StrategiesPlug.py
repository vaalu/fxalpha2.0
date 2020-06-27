import csv
from modules.props.ConfigProps import AppStrategyLogger
from modules.analytics.MACDStrategy import MACDStrategy
from modules.util.RedisUtil import RedisUtil
from modules.util.RedisStrategyUtil import RedisStrategyUtil

logger = AppStrategyLogger('StrategiesPlug')
class StrategiesPlug():
	__instance = None
	__strategies = [
		MACDStrategy.get_instance()
	]
	__equities, __commodities, __all_instruments = RedisUtil.get_instance().fetch_all_instruments()
	__red_stg_util = RedisStrategyUtil()
	__equities_spread = []
	__spread_targets = {}
	@staticmethod
	def get_instance():
		if StrategiesPlug.__instance == None:
			StrategiesPlug()
		return StrategiesPlug.__instance
	def __init__(self):
		if StrategiesPlug.__instance != None:
			raise Exception('StrategiesPlug is now singleton')
		else:
			StrategiesPlug.__instance = self
			for instrument in self.__all_instruments:
				instr_key = instrument["token"]
				for strategy in self.__strategies:
					self.__red_stg_util.create_bucket_if_none(strategy.get_name(), instr_key, 1)
					self.__red_stg_util.create_bucket_if_none(strategy.get_name(), instr_key, 5)
				if "CRUDE" in instrument["symbol"]:
					self.__spread_targets[instr_key] = {
						"entry":8, 
						"target":18,
						"apply_for":1
					}
				if "NATURALGAS" in instrument["symbol"]:
					self.__spread_targets[instr_key] = {
						"entry":0.3, 
						"target":1,
						"apply_for":5
					}
			try:
				logger.info('Reading spread info')
				with open('equity.spread.csv', 'r') as csv_file:
					decoded_content = csv_file.content.decode('utf-8')
					reader = csv.reader(decoded_content.splitlines(), delimiter=',')
					next(reader)
					self.__equities_spread = list(reader)
			except OSError as e:
				logger.debug('Unable to read spread file. Abandoning further requests. %s'%e)
	def process_on_tick(self, data):
		for strategy in self.__strategies:
			strategy.process(data)
	def analyze(self, instrument, duration, processing_time):
		prev_min = processing_time - 60 * duration
		entry_spread = self.__spread_targets[str(instrument)]["entry"] if str(instrument) in self.__spread_targets else 0
		target_spread = self.__spread_targets[str(instrument)]["target"] if str(instrument) in self.__spread_targets else 0
		apply_for = self.__spread_targets[str(instrument)]["apply_for"] if str(instrument) in self.__spread_targets else 0
		if entry_spread > 0 and target_spread > 0:
			for strategy in self.__strategies:
				curr_data, prev_data = self.__red_stg_util.fetch(strategy.get_name(), instrument, duration, processing_time, prev_min)
				bucket_01, bucket_05 = self.__red_stg_util.fetch_strategies(strategy.get_name(), instrument)
				bucket = bucket_01 if duration == 1 else bucket_05
				if duration == apply_for:
					bucket = strategy.analyze(instrument, duration, curr_data, prev_data, entry_spread, target_spread, bucket)
					bucket = self.__red_stg_util.save_bucket(bucket)

StrategiesPlug()