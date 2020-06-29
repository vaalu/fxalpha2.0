import redis
import json
from modules.props.ConfigProps import AppCacheLogger
logger = AppCacheLogger('RedisStrategyUtil')
class RedisStrategyUtil():
	__red = redis.Redis(host='localhost', port=6379, decode_responses=True)
	__reset_keys = ['high', 'low', 'macd', 'entry', 'trend', 'status', 'stoploss', 'sl_trigger', 'target', 'is_applied']
	def __init__(self):
		logger.info('RedisStrategyUtil')
	def create_bucket_if_none(self, strategy_id, instr, duration):
		strategy_bucket = 'STG:BKT:%s:%i:%s'%(strategy_id, duration, instr)
		bucket = {
			"id":strategy_bucket
		}
		self.__red.hmset(strategy_bucket, bucket)
		return bucket
	def reset(self, bucket):
		self.__red.hdel(bucket["id"], *self.__reset_keys)
		bucket = self.__red.hgetall(bucket["id"])
		# logger.info('Reset bucket %s '%bucket)
		return bucket
	def fetch_strategies(self, strategy_id, instr):
		strategy_bucket_01 = 'STG:BKT:%s:%i:%s'%(strategy_id, 1, instr)
		strategy_bucket_05 = 'STG:BKT:%s:%i:%s'%(strategy_id, 5, instr)
		stg_01 = self.__red.hgetall(strategy_bucket_01)
		stg_05 = self.__red.hgetall(strategy_bucket_05)
		return stg_01, stg_05
	def save_strategy(self, strategy_id, instr, duration, data):
		strategy_bucket = 'STG:BKT:%s:%i:%s'%(strategy_id, duration, instr)
		if data != None and data != {}:
			self.__red.hmset(strategy_bucket, data)
	def save_bucket(self, bucket):
		self.__red.hmset(bucket["id"], bucket)
	def fetch(self, instr, duration, curr_min, prev_min):
		curr_hkey = '%s:%iM:%i'%(instr, duration, curr_min)
		prev_hkey = '%s:%iM:%i'%(instr, duration, prev_min)
		keys_to_fetch = [curr_hkey, prev_hkey]
		curr_data = self.__red.hgetall(curr_hkey)
		prev_data = self.__red.hgetall(prev_hkey)
		return curr_data, prev_data # , bucket



