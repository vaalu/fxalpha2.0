import json
from modules.util.calc.RSI import RSI
from modules.util.calc.BollingerBands import BollingerBands
from modules.props.ConfigProps import AppLogger
from modules.util.RedisCalcUtil import RedisCalcUtil

logger = AppLogger('CalculationsUtil')
class CalculationsUtil():
	__bollinger = BollingerBands()
	__rsi_util = RSI()
	__dateutil = None
	__red_calc = None
	def __init__(self, dateutil):
		logger.info('Initializing calculations util')
		self.__dateutil = dateutil
		self.__red_calc = RedisCalcUtil()
	def __bollinger_bands(self, data):
		# logger.info('Bollinger bands')
		populated = []
		to_be_returned = []
		keys = []
		if data != None and len(data) > 0:
			boll_data = data[0:self.__bollinger.get_period()]
			boll_data.reverse()
			keys, populated = self.__bollinger.calculate(boll_data)
			populated.reverse()
			remaining = data[self.__bollinger.get_period():]
			to_be_returned.extend(populated)
			to_be_returned.extend(remaining)
		return keys, to_be_returned
	def __rsi(self, data):
		# logger.info('RSI')
		populated = []
		to_be_returned = []
		keys = []
		if data != None and len(data) > 0:
			rsi_data = data[0:self.__rsi_util.get_period()]
			rsi_data.reverse()
			keys, populated = self.__rsi_util.calculate(rsi_data)
			populated.reverse()
			remaining = data[self.__rsi_util.get_period():]
			to_be_returned.extend(populated)
			to_be_returned.extend(remaining)
		return keys, to_be_returned
	def __stochastic(self):
		logger.info('Stochastic')
	def __macd(self):
		logger.info('MACD')
	def __histogram(self):
		logger.info('Histogram')
	def __supertrend(self):
		logger.info('Supertrend')
	def __awesome(self):
		logger.info('Awesome oscillator')
	def calculate_1_min(self, instrument, keys_patterns):
		# logger.info('Key patterns to be fetched: %s'%keys_patterns)
		data = self.__red_calc.fetch_data(instrument, keys_patterns)
		calc_keys = []
		if len(data) > 0 and len(data) < 40:
			substitute = data[len(data)-1]
			count = len(data)
			for index in range(count, 40):
				data.append(substitute)
		
		bb_keys, bollinger_processed = self.__bollinger_bands(data)
		calc_keys.extend(bb_keys)
		
		rsi_keys, rsi_processed = self.__rsi(bollinger_processed)
		calc_keys.extend(rsi_keys)
		if len(rsi_processed) > 0:
			self.__red_calc.save_processed(calc_keys, rsi_processed[0])
			# logger.info('Calculations saved successfully: %s'%rsi_processed[0]["instrument"])
