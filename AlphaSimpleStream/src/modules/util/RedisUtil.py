import redis
import json
from modules.props.ConfigProps import AppLogger
from modules.util.OHLCSingleItemProcessor import OHLCSingleItemProcessor
from modules.util.OHLCItemProcessor import OHLCItemProcessor

logger = AppLogger()

class RedisUtil():
	__red = redis.Redis(host='localhost', port=6379, decode_responses=True)
	__cache_it = {"duration":"0M"}
	__instrument_types = {
		"NSE":"EQUITY",
		"BSE":"EQUITY",
		"MCX":"COMMODITIES"
	}
	def __init__(self):
		logger.debug('Initializing redis util')
		def save_to_cache(source_val):
			hset_key = source_val["instrument"]
			self.__red.hset(hset_key, "instrument", source_val["instrument"])
			self.__red.hset(hset_key, "instrument_key", source_val["instrument_key"])
			self.__red.hset(hset_key, "open", source_val["open"])
			self.__red.hset(hset_key, "high", source_val["high"])
			self.__red.hset(hset_key, "low", source_val["low"])
			self.__red.hset(hset_key, "close", source_val["close"])
			zkey = 'OHLC:KEY:%s:%s'%(self.__cache_it["duration"],source_val["instrument_key"])
			logger.info('ZKey: %s : tstamp: %s'%(zkey, source_val))
			self.__red.zadd(zkey, {hset_key:float(source_val["timestamp"])})
		self.__cache_it["save"] = save_to_cache
	
	def add_processing_instruments(self, instruments):
		for instrument in instruments:
			hset_key = 'INSTRUMENT:%s:%s'%(self.__instrument_types[instrument["exchange"]], instrument["token"])
			self.__red.hset(hset_key, "token", instrument["token"])
			self.__red.hset(hset_key, "symbol", instrument["symbol"])
			self.__red.hset(hset_key, "name", instrument["name"])
			self.__red.hset(hset_key, "expiry", instrument["expiry"])

	def split_get_keys(self, instr_key, start_tstamp, end_tstamp):
		hset_keys = list([])
		remaining = end_tstamp % 30
		while start_tstamp <= end_tstamp:
			keys = self.__red.zrangebyscore("%s:instrument_keys"%instr_key, start_tstamp, start_tstamp+30)
			hset_keys.extend(keys)
			start_tstamp = start_tstamp+30
		start_tstamp-30
		if remaining > 0:
			keys = self.__red.zrangebyscore("%s:instrument_keys"%instr_key, start_tstamp, start_tstamp+remaining)
			hset_keys.extend(keys)
		return hset_keys

	def split_get_keys_5(self, instr_key, start_tstamp, end_tstamp):
		hset_keys = list([])
		remaining = end_tstamp % 30
		zkey = 'OHLC:KEY:1M:%s'%(instr_key)
		logger.info('Key: %s'%zkey)
		while start_tstamp <= end_tstamp:
			keys = self.__red.zrangebyscore(zkey, start_tstamp, start_tstamp+30)
			hset_keys.extend(keys)
			start_tstamp = start_tstamp+30
		start_tstamp-30
		if remaining > 0:
			keys = self.__red.zrangebyscore(zkey, start_tstamp, start_tstamp+remaining)
			hset_keys.extend(keys)
		return hset_keys

	def fetch_between(self, instr_key, start_tstamp, end_tstamp, duration_key):
		index_tsamp = start_tstamp
		split_search = 2 if end_tstamp%2 == 0 else 1
		hset_keys = self.split_get_keys(instr_key, start_tstamp, end_tstamp)
		logger.info('Total number of keys present: %i'%(len(hset_keys)))
		if hset_keys != None and len(hset_keys) > 0:
			item_processor = OHLCSingleItemProcessor(instr_key)
			ohlc_data = {}
			for key in hset_keys:
				cache_item = self.__red.hgetall(key)
				if cache_item != None and cache_item != {}:
					ohlc_data = item_processor.calculate_ohlc(int(cache_item["instrument_token"]), "%s:%i"%(duration_key, start_tstamp), start_tstamp, cache_item)
				# Delete previously processed keys. Mark the keys for deletion
				self.__red.set("KEYS:MARK:DEL:%s"%key, key)
			if ohlc_data != {}:
				item_processor.final_save(self.__cache_it["save"])
			self.__cache_it["duration"]=duration_key

	def fetch_between_5(self, instr_key, start_tstamp, end_tstamp, duration_key):
		index_tsamp = start_tstamp
		split_search = 2 if end_tstamp%2 == 0 else 1
		hset_keys = self.split_get_keys_5(instr_key, start_tstamp, end_tstamp)
		logger.info('Total number of keys present: %i'%(len(hset_keys)))
		if hset_keys != None and len(hset_keys) > 0:
			item_processor = OHLCItemProcessor(instr_key)
			ohlc_data = {}
			for key in hset_keys:
				cache_item = self.__red.hgetall(key)
				if cache_item != None and cache_item != {}:
					logger.info('%s # %s # %i %s'%(cache_item["instrument"], "%s:%i"%(duration_key, start_tstamp), start_tstamp, cache_item))
					ohlc_data = item_processor.calculate_ohlc(instr_key, "%s:%i"%(duration_key, start_tstamp), start_tstamp, cache_item)
			print(ohlc_data)
			if ohlc_data != {}:
				item_processor.final_save(self.__cache_it["save"])
			self.__cache_it["duration"]=duration_key

	def fetch_all(self, instr_key, tstamp):
		hset_key = '%s:%s*'%(instr_key,tstamp)
		logger.debug('HSET Key: %s'%hset_key)
		keys = self.__red.keys(hset_key)
		logger.debug(keys)
		if len(keys) > 0:
			instr_val = '%s:%s'%(tstamp, instr_key)
			item_processor = OHLCSingleItemProcessor(instr_val)
			ohlc_data = {}
			for key in keys:
				cache_item = self.__red.hgetall(key)
				if cache_item != None:
					ohlc_data = item_processor.calculate_ohlc(int(cache_item["instrument_token"]), "1M:%i"%(start_tstamp), int(cache_item["last_traded_time"]), cache_item)
			if ohlc_data != {}:
				item_processor.final_save(self.__cache_it["save"])
	
	def split_as_batch(self, iterable, batch_size):
		for indx in range(0, len(iterable), batch_size):
			yield iterable[indx:indx + batch_size]
	
	def eod_process(self, instrument, duration):
		key_pattern = '%s:%iM:*'%(str(instrument), duration)
		split_eod_keys = self.split_as_batch(self.__red.keys(key_pattern), 100)
		items_to_save = list([])
		for batch in split_eod_keys:
			for key in batch:
				cache_item = self.__red.hgetall(key)
				items_to_save.append(cache_item)
		return items_to_save

	def remove_processed(self):
		logger.info('Removing all processed keys')
		processed_keys = list([])
		split_keys = self.split_as_batch(self.__red.keys("KEYS:MARK:DEL*"), 500)
		index = 0
		for ind in split_keys:
			index = index + 1
		logger.info('Total count %i'%index)
		split_keys = self.split_as_batch(self.__red.keys("KEYS:MARK:DEL*"), 500)
		for batch in split_keys:
			split_keys_del = list([])
			for key in batch:
				self.__red.delete(self.__red.get(key))
				self.__red.delete(key)
			index = index-1
			logger.info('Deleting from cache. Remaining batches: %i'%index)