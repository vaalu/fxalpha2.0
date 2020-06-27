import json
import redis
import datetime
from modules.props.ConfigProps import AppStreamLogger
from modules.util.DateTimeUtil import DateTimeUtil
from modules.analytics.StrategiesPlug import StrategiesPlug

logger = AppStreamLogger.get_instance()

class DefaultMessageHandlerLegacy():
	__red = redis.Redis(host='localhost', port=6379)
	__date_util = DateTimeUtil.get_instance()
	__start, __eq_end, __end = __date_util.get_market_timings()
	__strategy = StrategiesPlug.get_instance()
	def __init__(self):
		self.__start, self.__eq_end, self.__end = self.__date_util.get_market_timings()
	def __now_time(self):
		return self.__date_util.get_current_local_time()
	def __getCache(self):
		return self.__red
	
	def __defaultHandler(self, message={}):
		# Initialize cache
		red = self.__getCache()
		# Read value from message and store in cache for further processing
		source_val = message
		etstamp = source_val["exchange_timestamp"] if self.__start <= int(source_val["exchange_timestamp"]) <= self.__end else self.__now_time() 
		# etstamp = self.__now_time()
		curr_ts = float(etstamp) + ((datetime.datetime.now().microsecond % 100000)/100000)
		source_val["exchange_timestamp"] = etstamp
		hset_key = '%s:%s:%s'%(source_val["instrument_token"], etstamp, curr_ts)
		red.hmset(hset_key, source_val)
		logger.info('%s : %s : %s'%(hset_key, etstamp, source_val["last_traded_price"]))
		# ZRange for retrieving from cache based on time
		zkey = '%s:instrument_keys'%(source_val["instrument_token"])
		red.zadd(zkey, {hset_key:curr_ts})
		self.__strategy.process_on_tick(source_val)
	
	def handle(self, message={}):
		# Handle message with default handler for now. May need to update later
		self.__defaultHandler(message)
		

