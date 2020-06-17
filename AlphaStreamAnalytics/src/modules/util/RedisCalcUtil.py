import redis
from modules.props.ConfigProps import AppCacheLogger
logger = AppCacheLogger('RedisCalcUtil')

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