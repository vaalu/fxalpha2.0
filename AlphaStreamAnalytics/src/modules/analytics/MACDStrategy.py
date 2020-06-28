from modules.props.ConfigProps import AppStrategyLogger
from modules.util.RedisStrategyUtil import RedisStrategyUtil
from modules.util.TeleBotUtil import TeleBotUtil

logger = AppStrategyLogger('MACDStrategy')
class MACDStrategy():
	__red_stg_util = RedisStrategyUtil()
	__strategy_id = 'MACD'
	__store = {}
	__name = "MACD"
	__telebot = TeleBotUtil.get_instance()
	__instance = None
	@staticmethod
	def get_instance():
		if MACDStrategy.__instance == None:
			MACDStrategy()
		return MACDStrategy.__instance
	def __init__(self):
		print('MACD Strategy')
		if MACDStrategy.__instance != None:
			raise Exception('MACD Strategy is now singleton')
		else:
			MACDStrategy.__instance = self
			self.__telebot.send_message_01('MACD strategy initialized')
	def get_name(self):
		return self.__name
	def invalidate(self, bucket):
		logger.info('INVALIDATED|%s'%(bucket))
		self.__telebot.send_message_01('INVALIDATED|%s'%bucket)
		return self.__red_stg_util.reset(bucket)
	def stoploss(self, trend, ltp, bucket):
		logger.info('Stoploss: %s: %f: %s'%(trend, ltp, bucket))
		self.__telebot.send_message_01('Stoploss: %s: %f: %s'%(trend, ltp, bucket))
		bucket["status"] = "STOP"
		return bucket
	def completed(self, ltp, bucket):
		bucket = self.__red_stg_util.reset(bucket)
		logger.info('COMPLETED|%f:%s'%(ltp,bucket))
		self.__telebot.send_message_01('COMPLETED|%f:%s'%(ltp,bucket))
		return bucket
	def process_bucket(self, data, bucket, duration):
		ltp = float(data["last_traded_price"])
		trend = bucket["trend"] if "trend" in bucket else ""
		target = float(bucket["target"]) if "target" in bucket else ltp
		target_spread = float(bucket["target_spread"]) if "target_spread" in bucket else ltp 
		stoploss = float(bucket["stoploss"]) if "stoploss" in bucket else 0
		entry = float(bucket["entry"]) if "entry" in  bucket else ltp
		if trend == "long" and ltp > entry and ("target" not in bucket):
			bucket["status"] = "RUNNING"
			bucket["target"] = ltp + float(bucket["target_spread"])
		elif trend == "short" and ltp < entry and ("target" not in bucket):
			bucket["status"] = "RUNNING"
			bucket["target"] = ltp - float(bucket["target_spread"])
		elif trend == "long" and ltp > target:
			logger.info('Target completed: LONG: %f : %s'%(ltp, bucket))
			bucket = self.completed(ltp,bucket)
		elif trend == "short" and ltp < target:
			logger.info('Target completed: SHORT: %f : %s'%(ltp, bucket))
			bucket = self.completed(ltp,bucket)
		elif trend == "long" and ltp < stoploss:
			logger.info('Stoploss completed: LONG: %f : %s'%(ltp, bucket))
			bucket = self.stoploss('LONG', ltp, bucket)
		elif trend == "short" and ltp < stoploss:
			bucket = self.stoploss('SHORT', ltp, bucket)
		self.__red_stg_util.save_bucket(bucket)
	def process(self, data):
		instr = data["instrument_token"]
		bucket_01, bucket_05 = self.__red_stg_util.fetch_strategies(self.__name, instr)
		if bucket_01 != None:
			self.process_bucket(data, bucket_01, 1)
		if bucket_05 != None:
			self.process_bucket(data, bucket_05, 5)

	def analyze(self, instr, duration, curr_data, prev_data, entry_spread, target_spread, bucket):
		def find_buffer(cdata, pdata, bucket):
			logger.info('Finding buffer %s:%s:%s'%(cdata, pdata, bucket))
			status = bucket["status"] if "status" in bucket else ""
			if "status" not in bucket or "RUNNING" != bucket["status"]:
				if "long" == bucket["trend"] and float(cdata["high"]) > float(bucket["high"]) and float(cdata["macd"]) > 0 and status != "SIGNAL":
					bucket["entry"] = float(cdata["high"]) + entry_spread
					bucket["status"] = "SIGNAL"
				elif "short" == bucket["trend"] and float(cdata["low"]) < float(bucket["low"]) and float(cdata["macd"]) < 0 and status != "SIGNAL":
					bucket["entry"] = float(cdata["low"]) - entry_spread
					bucket["status"] = "SIGNAL"
				elif ("long" == bucket["trend"] and float(cdata["macd"]) < 0) or ("short" == bucket["trend"] and float(cdata["macd"]) > 0):
					return self.invalidate(bucket)
			else:
				macd = float(cdata["macd"]) if "macd" in cdata else 0
				if "long" == bucket["trend"] and macd < 0:
					bucket["stoploss"] = float(cdata["low"]) - entry_spread
				elif "short" == bucket["trend"] and macd > 0:
					bucket["stoploss"] = float(cdata["high"]) + entry_spread
			return bucket
		def find_trend(cdata, pdata, bucket):
			# logger.info('Finding trend %s:%s:%s'%(cdata, pdata, bucket))
			trend = bucket["trend"] if "trend" in bucket else ""
			status = bucket["status"] if "status" in bucket else ""
			if status != "" and status == "STOP":
				if trend == "long":
					bucket["trend"] = "short"
					trend = "short"
				if trend == "short":
					bucket["trend"] = "long"
					trend = "long"
				bucket["high"] = cdata["high"]
				bucket["low"] = cdata["low"]
				bucket["macd"] = cdata["macd"]
				bucket["spread"] = entry_spread
				bucket["target_spread"] = target_spread
			if trend == "invalidated" or trend == "stoploss":
				bucket = self.__red_stg_util.reset(bucket)
			if "trend" not in bucket or trend == "":
				logger.info('Freshly checking after invalidate %s'%bucket)
				curr_macd = float(cdata["macd"]) if cdata != None and "macd" in cdata else 0
				prev_macd = float(pdata["macd"]) if pdata != None and "macd" in pdata else 0
				if curr_macd > 0 and prev_macd < 0:
					bucket["trend"] = "long"
				if curr_macd < 0 and prev_macd > 0:
					bucket["trend"] = "short"
				if "trend" in bucket:
					bucket["high"] = cdata["high"]
					bucket["low"] = cdata["low"]
					bucket["macd"] = cdata["macd"]
					bucket["spread"] = entry_spread
					bucket["target_spread"] = target_spread
					return find_buffer(cdata, pdata, bucket)
			else:
				return find_buffer(cdata, pdata, bucket)
			return bucket
		return find_trend(curr_data, prev_data, bucket)
MACDStrategy()




















