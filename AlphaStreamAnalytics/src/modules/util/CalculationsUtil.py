from modules.props.ConfigProps import AppLogger
logger = AppLogger('CalculationsUtil')
class CalculationsUtil():
	def __init__(self):
		logger.info('Initializing calculations util')
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
	def __awesome(self):
		logger.info('Awesome oscillator')