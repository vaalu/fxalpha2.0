import json
from modules.util.calc.RSI import RSI
from modules.util.calc.BollingerBands import BollingerBands
from modules.util.calc.MACD import MACD
from modules.util.calc.AwesomeOscillator import AwesomeOscillator
from modules.util.calc.KeltnerChannel import KeltnerChannel
from modules.props.ConfigProps import AppLogger
from modules.util.RedisCalcUtil import RedisCalcUtil

logger = AppLogger('CalculationsUtil')
class CalculationsUtil():
	__bollinger = BollingerBands()
	__rsi_util = RSI()
	__macd_util = MACD()
	__awesome_osc = AwesomeOscillator()
	__kc = KeltnerChannel()
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
	def __keltner(self, data):
		populated = []
		to_be_returned = []
		keys = []
		if data != None and len(data) > 0:
			__n_period, __n_atr = self.__kc.get_config()
			kc_data = data[0:__n_period]
			kc_data.reverse()
			keys, populated = self.__rsi_util.calculate(kc_data)
			populated.reverse()
			remaining = data[__n_period:]
			to_be_returned.extend(populated)
			to_be_returned.extend(remaining)
		return keys, to_be_returned
	def __macd(self, data):
		# logger.info('MACD')
		populated = []
		to_be_returned = []
		keys = []
		__n_slow, __n_fast, __n_sign = self.__macd_util.get_config()
		if data != None and len(data) > 0:
			macd_data = data[0:__n_slow]
			macd_data.reverse()
			keys, populated = self.__macd_util.calculate(macd_data)
			populated.reverse()
			remaining = data[__n_slow:]
			to_be_returned.extend(populated)
			to_be_returned.extend(remaining)
		return keys, to_be_returned
	def __histogram(self):
		logger.info('Histogram')
	def __supertrend(self):
		logger.info('Supertrend')
	def __awesome(self, data):
		# logger.info('Awesome oscillator')
		populated = []
		to_be_returned = []
		keys = []
		short_period, long_period = self.__awesome_osc.get_config()
		if data != None and len(data) > 0:
			ao_data = data[0:long_period]
			ao_data.reverse()
			keys, populated = self.__awesome_osc.calculate(ao_data)
			populated.reverse()
			remaining = data[long_period:]
			to_be_returned.extend(populated)
			to_be_returned.extend(remaining)
		return keys, to_be_returned
	def calculate(self, instrument, keys_patterns):
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

		macd_keys, macd_processed = self.__macd(rsi_processed)
		calc_keys.extend(macd_keys)

		ao_keys, ao_processed = self.__awesome(macd_processed)
		calc_keys.extend(ao_keys)

		kc_keys, kc_processed = self.__keltner(ao_processed)
		calc_keys.extend(kc_keys)

		if len(kc_processed) > 0:
			self.__red_calc.save_processed(calc_keys, kc_processed[0])
			# logger.info('Saved: %s:%s:MACD:%s'%(ao_processed[0]["instrument"],ao_processed[0]["close"], ao_processed[0]["macd"]))
