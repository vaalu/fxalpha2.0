import csv
from modules.props.ConfigProps import AppStrategyLogger
from modules.analytics.MACDStrategy import MACDStrategy
from modules.util.RedisUtil import RedisUtil
from modules.util.RedisStrategyUtil import RedisStrategyUtil
from modules.util.DateTimeUtil import DateTimeUtil

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
	__date_util = DateTimeUtil.get_instance()
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
						"symbol":instrument["symbol"], 
						"apply_for":1
					}
				if "NATURALGAS" in instrument["symbol"]:
					self.__spread_targets[instr_key] = {
						"entry":0.3, 
						"target":1,
						"symbol":instrument["symbol"], 
						"apply_for":5
					}
			try:
				logger.info('Reading spread info')
				with open('equities.spread.csv', 'r') as csv_file:
					reader = csv.reader(csv_file)
					next(reader)
					for row in reader:
						prepared_spread = {}
						prepared_spread["price_range"]=float(row[0])
						prepared_spread["spread"]=float(row[1])
						prepared_spread["target"]=float(row[2])
						prepared_spread["apply_for"]=5
						self.__equities_spread.append(prepared_spread)
			except OSError as e:
				logger.debug('Unable to read spread file. Abandoning further requests. %s'%e)
			logger.info('Equities spread info: %s'%self.__equities_spread)
			start_time, eq_end, cm_end = self.__date_util.get_market_timings()
			for equity in self.__equities:
				instr_token = equity["token"]
				prev_time = start_time - 60 * 5
				curr_data, prev_data = self.__red_stg_util.fetch(instr_token, 5, int(start_time), int(prev_time))
				indx = 1
				next_spread = self.__equities_spread[indx]
				for spread_info in self.__equities_spread:
					if float(spread_info["price_range"]) < float(curr_data["close"]):
						self.__spread_targets[instr_token] = {
							"entry":next_spread["spread"], 
							"target":next_spread["target"],
							"symbol":equity["symbol"], 
							"closing_price":curr_data["close"], 
							"apply_for":5
						}
					logger.info('%i : %i'%(indx, len(self.__equities_spread)))
					if (indx+1) < len(self.__equities_spread):
						indx = indx + 1
					next_spread = self.__equities_spread[indx]
					
				
			logger.info(self.__spread_targets)

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
				curr_data, prev_data = self.__red_stg_util.fetch(instrument, duration, processing_time, prev_min)
				bucket_01, bucket_05 = self.__red_stg_util.fetch_strategies(strategy.get_name(), instrument)
				bucket = bucket_01 if duration == 1 else bucket_05
				if duration == apply_for:
					bucket = strategy.analyze(instrument, duration, curr_data, prev_data, entry_spread, target_spread, bucket)
					bucket = self.__red_stg_util.save_bucket(bucket)

StrategiesPlug()