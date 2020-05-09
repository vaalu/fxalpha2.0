import json
import redis
from modules.props.ConfigProps import AppLogger

logger = AppLogger()

class DefaultMessageHandler():
	red = redis.Redis(host='localhost', port=6379)
	def __init__(self):
		logger.info('Initializing by default')
	
	def __defaultHandler(self, message={}, handler=None):
		# Initialize cache
		# Read value from message and store in cache for further processing
		def save_to_cache(source_val):
			logger.info(source_val)
			hset_key = source_val["instrument"]
			self.red.hset(hset_key, "instrument", source_val["instrument"])
			self.red.hset(hset_key, "open", source_val["open"])
			self.red.hset(hset_key, "high", source_val["high"])
			self.red.hset(hset_key, "low", source_val["low"])
			self.red.hset(hset_key, "close", source_val["close"])
			self.red.hset(hset_key, "timestamp", source_val["timestamp"])
		
		instr_msg = json.loads(message.value)
		if handler != None:
			handler.calculate_ohlc(instr_msg["instrument_token"], instr_msg["exchange_timestamp"], instr_msg, callback=save_to_cache)
		
	def handle(self, message={}, handler=None):
		# Handle message with default handler for now. May need to update later
		self.__defaultHandler(message, handler)
		