import json
import redis
import time
import datetime
from dateutil import tz
from modules.props.ConfigProps import AppLogger
from modules.util.SingleInstanceUtil import SingleInstanceUtil

logger = AppLogger('DefaultMessageHandlerLegacy')

class DefaultMessageHandlerLegacy():
	__red = redis.Redis(host='localhost', port=6379)
	__start = 0
	__end = 0
	__offset = 0
	def __init__(self):
		print('Initializing by default')
		self.__start, self.__end, self.__offset = SingleInstanceUtil().today_timings()
	def __now_time(self):
		return time.mktime(datetime.datetime.now().timetuple()) - self.__tz_offset()
	def __getCache(self):
		return self.__red;
	
	def __defaultHandler(self, message={}):
		# Initialize cache
		red = self.__getCache()
		# Read value from message and store in cache for further processing
		source_val = message
		# Process message
		etstamp = source_val["exchange_timestamp"] if self.__start <= int(source_val["exchange_timestamp"]) <= self.__end else self.__now_time() 
		curr_ts = float(etstamp) + ((datetime.datetime.now().microsecond % 100000)/100000)
		hset_key = '%s:%s:%s'%(source_val["instrument_token"], etstamp, curr_ts)
		red.hset(hset_key, "exchange_timestamp", etstamp)
		red.hset(hset_key, "instrument_token", source_val["instrument_token"])
		red.hset(hset_key, "last_traded_price", source_val["last_traded_price"])
		red.hset(hset_key, "last_traded_time", source_val["last_traded_time"])
		logger.info('%s : %s : %s'%(hset_key, etstamp, source_val["last_traded_price"]))
		red.hset(hset_key, "last_traded_quantity", source_val["last_traded_quantity"])
		red.hset(hset_key, "trade_volume", source_val["trade_volume"])
		red.hset(hset_key, "best_bid_price", source_val["best_bid_price"])
		red.hset(hset_key, "best_bid_quantity", source_val["best_bid_quantity"])
		red.hset(hset_key, "best_ask_price", source_val["best_ask_price"])
		red.hset(hset_key, "best_ask_quantity", source_val["best_ask_quantity"])
		red.hset(hset_key, "total_buy_quantity", source_val["total_buy_quantity"])
		red.hset(hset_key, "total_sell_quantity", source_val["total_sell_quantity"])
		red.hset(hset_key, "average_trade_price", source_val["average_trade_price"])
		red.hset(hset_key, "exchange_timestamp", etstamp)
		red.hset(hset_key, "open_price", source_val["open_price"])
		red.hset(hset_key, "high_price", source_val["high_price"])
		red.hset(hset_key, "low_price", source_val["low_price"])
		red.hset(hset_key, "close_price", source_val["close_price"])
		red.hset(hset_key, "yearly_high_price", source_val["yearly_high_price"])
		red.hset(hset_key, "yearly_low_price", source_val["yearly_low_price"])
		zkey = '%s:instrument_keys'%(source_val["instrument_token"])
		red.zadd(zkey, {hset_key:curr_ts})
	
	def handle(self, message={}):
		# Handle message with default handler for now. May need to update later
		self.__defaultHandler(message)
		

