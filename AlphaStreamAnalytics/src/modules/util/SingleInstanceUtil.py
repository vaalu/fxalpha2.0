from modules.props.ConfigProps import AppLogger, AppProps
from modules.util.AliceInstrumentsUtil import AliceInstruments

logger = AppLogger()
class SingleInstanceUtil():
	__alice_instruments = AliceInstruments()
	def __init__(self):
		logger.info('Initializing singleton instances for the application')
	def get_instrument_util(self):
		return self.__alice_instruments
