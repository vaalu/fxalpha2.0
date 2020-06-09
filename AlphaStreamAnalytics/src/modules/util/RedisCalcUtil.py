import redis
import json
from datetime import datetime
from modules.props.ConfigProps import AppLogger
logger = AppLogger('RedisCalcUtil')

class RedisCalcUtil():
	__red = redis.Redis(host='localhost', port=6379, decode_responses=True)
	def __init__(self):
		logger.info('Redis calculations util initialization')
	def fetch_data_1_min(self, instrument)