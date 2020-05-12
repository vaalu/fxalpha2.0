import redis
import json
from modules.props.ConfigProps import AppLogger
from modules.util.OHLCSingleItemProcessor import OHLCSingleItemProcessor

logger = AppLogger()

class RedisUtil():
	__red = redis.Redis(host='localhost', port=6379, decode_responses=True)
	__cache_it = {}
	def __init__(self):
		logger.debug('Initializing redis util')
		def save_to_cache(source_val):
			logger.info(source_val)
			hset_key = source_val["instrument"]
			self.__red.hset(hset_key, "instrument", source_val["instrument"])
			self.__red.hset(hset_key, "open", source_val["open"])
			self.__red.hset(hset_key, "high", source_val["high"])
			self.__red.hset(hset_key, "low", source_val["low"])
			self.__red.hset(hset_key, "close", source_val["close"])
			self.__red.hset(hset_key, "timestamp", source_val["timestamp"])
			self.__red.hset(hset_key, "isotimestamp", source_val["timestamp"])
		self.__cache_it["save"] = save_to_cache
	
	def fetch_between(self, instr_key, start_tstamp, end_tstamp):
		index_tsamp = start_tstamp
		hset_keys = self.__red.zrangebyscore("%s:instrument_keys"%instr_key, start_tstamp, end_tstamp)
		print(hset_keys)
		if hset_keys != None and len(hset_keys) > 0:
			item_processor = OHLCSingleItemProcessor(instr_key)
			ohlc_data = {}
			for key in hset_keys:
				cache_item = self.__red.hgetall(key)
				if cache_item != None:
					ohlc_data = item_processor.calculate_ohlc(int(cache_item["instrument_token"]), "1M:%i"%(start_tstamp), int(cache_item["exchange_timestamp"]), cache_item)
			if ohlc_data != {}:
				item_processor.final_save(self.__cache_it["save"])

	def fetch_all(self, instr_key, tstamp):
		hset_key = '%s:%s*'%(instr_key,tstamp)
		print('HSET Key: ', hset_key)
		keys = self.__red.keys(hset_key)
		print('List of keys', keys)
		if len(keys) > 0:
			instr_val = '%s:%s'%(tstamp, instr_key)
			item_processor = OHLCSingleItemProcessor(instr_val)
			ohlc_data = {}
			for key in keys:
				cache_item = self.__red.hgetall(key)
				if cache_item != None:
					ohlc_data = item_processor.calculate_ohlc(int(cache_item["instrument_token"]), int(cache_item["exchange_timestamp"]), cache_item)
			if ohlc_data != {}:
				item_processor.final_save(self.__cache_it["save"])
