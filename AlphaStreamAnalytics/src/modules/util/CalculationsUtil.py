from modules.util.calc.BollingerBands import BollingerBands
from modules.props.ConfigProps import AppLogger
from modules.util.RedisCalcUtil import RedisCalcUtil

logger = AppLogger('CalculationsUtil')

class CalculationsUtil():
	__bollinger = BollingerBands()
	__dateutil = None
	def __init__(self, dateutil):
		logger.info('Initializing calculations util')
		self.__dateutil = dateutil
	def __rsi(self):
		logger.info('RSI')
	def __stochastic(self):
		logger.info('Stochastic')
	def __macd(self):
		logger.info('MACD')
	def __histogram(self):
		logger.info('Histogram')
	def __supertrend(self):
		logger.info('Supertrend')
	def __bollinger_bands(self):
		logger.info('Bollinger bands')
		period = self.__bollinger.get_period()
	def __awesome(self):
		logger.info('Awesome oscillator')
	def calculate_1_min(self, instrument, keys_patterns):
		logger.info('Performing calculations for instrument: %s'%str(keys_patterns))
