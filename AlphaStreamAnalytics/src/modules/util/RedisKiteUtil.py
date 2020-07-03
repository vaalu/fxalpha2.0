import redis
from modules.props.ConfigProps import AppCacheLogger
logger = AppCacheLogger('RedisKiteUtil')

class RedisCalcUtil():
	__red = redis.Redis(host='localhost', port=6379, decode_responses=True)
	def __init__(self):
		logger.info('Redis calculations util initialization')
	
	def save_processed(self, calc_keys, source_val):
			hset_key = source_val["instrument"]
			for key in calc_keys:
				if key in source_val:
					saved = self.__red.hset(hset_key, key, source_val[key])
					# logger.info('key: %s | %s | %f'%(hset_key, key, source_val[key]))
	def fetch_data(self, instrument, keys):
		data = []
		for key in keys:
			datum = self.__red.hgetall(key)
			if datum != None and datum != {}:
				datum["close"] = float(datum["close"])
				datum["high"] = float(datum["high"])
				datum["low"] = float(datum["low"])
				data.append(datum)
		return data
	def save_imported(self, data):
		for datum in data:
			rkey = datum["instrument"]
			split_key = rkey.split(':')
			duration = split_key[1]
			timestamp = split_key[2]
			instr_key = datum["instrument_key"]
			saved = self.__red.hmset(rkey, datum)
			zkey = 'OHLC:KEY:%s:%s'%(duration,instr_key)
			self.__red.zadd(zkey, {rkey:float(timestamp)})
