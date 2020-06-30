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
	__spread_info = {}
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
			self.__telebot.send_message_01('Program started')
	def get_name(self):
		return self.__name
	def spread_info(self, spread_info):
		self.__spread_info = spread_info
	def invoke_bot_message(self, message):
		self.__telebot.send_message_01(message)
	def invalidate(self, bucket):
		trend = bucket["trend"] if "trend" in bucket else "NA"
		status= bucket["status"] if "status" in bucket else "NA"
		instr = bucket["id"].split(":")
		name = self.__spread_info[instr[4]]["symbol"] if instr[4] in self.__spread_info else instr[4]
		duration = instr[3]
		self.invoke_bot_message('INVALIDATED : %s : %s min : trend : %s : status : %s'%(name, duration, trend, status))
		return self.__red_stg_util.reset(bucket)
	def stoploss(self, trend, ltp, bucket):
		logger.info('Stoploss: %s: %f: %s'%(trend, ltp, bucket))
		trend = bucket["trend"] if "trend" in bucket else "NA"
		status= bucket["status"] if "status" in bucket else "NA"
		instr = bucket["id"].split(":")
		name = self.__spread_info[instr[4]]["symbol"] if instr[4] in self.__spread_info else instr[4]
		duration = instr[3]
		self.invoke_bot_message('STOPLOSS : %s : %s min : trend : %s : status : %s : LTP : %f'%(name, duration, trend, status, ltp))
		bucket["status"] = "STOP"
		return self.__red_stg_util.reset(bucket)
	def completed(self, ltp, bucket):
		bucket = self.__red_stg_util.reset(bucket)
		logger.info('COMPLETED|%f:%s'%(ltp,bucket))
		trend = bucket["trend"] if "trend" in bucket else "NA"
		status= bucket["status"] if "status" in bucket else "NA"
		instr = bucket["id"].split(":")
		name = self.__spread_info[instr[4]]["symbol"] if instr[4] in self.__spread_info else instr[4]
		duration = instr[3]
		self.invoke_bot_message('COMPLETED : %s : %s min : trend : %s : status : %s : LTP : %f'%(name, duration, trend, status, ltp))
		return self.__red_stg_util.reset(bucket)
	def process_bucket(self, data, bucket, duration):
		ltp = float(data["last_traded_price"])
		trend = bucket["trend"] if "trend" in bucket else ""
		target = float(bucket["target"]) if "target" in bucket else ltp
		target_spread = float(bucket["target_spread"]) if "target_spread" in bucket else ltp 
		stoploss = float(bucket["stoploss"]) if "stoploss" in bucket else 0
		entry = float(bucket["entry"]) if "entry" in  bucket else ltp
		status = bucket["status"] if "status" in bucket else ""
		if trend == "long" and ltp > entry and ("target" not in bucket) and status != "RUNNING":
			bucket["status"] = "RUNNING"
			bucket["target"] = entry + float(bucket["target_spread"])
			instr = bucket["id"].split(":")
			name = self.__spread_info[instr[4]]["symbol"] if instr[4] in self.__spread_info else instr[4]
			duration = instr[3]
			self.invoke_bot_message('RUNNING (LONG): %s : %s min : LTP : %f : TARGET : %s'%(name, duration, ltp, bucket["target"]))
		elif trend == "short" and ltp < entry and ("target" not in bucket) and status != "RUNNING":
			bucket["status"] = "RUNNING"
			bucket["target"] = entry - float(bucket["target_spread"])
			instr = bucket["id"].split(":")
			name = self.__spread_info[instr[4]]["symbol"] if instr[4] in self.__spread_info else instr[4]
			duration = instr[3]
			self.invoke_bot_message('RUNNING (SHORT): %s : %s min : LTP : %f : TARGET : %s'%(name, duration, ltp, bucket["target"]))
		elif trend == "long" and ltp >= target:
			logger.info('Target completed: LONG: %f : %s'%(ltp, bucket))
			bucket = self.completed(ltp,bucket)
		elif trend == "short" and ltp <= target:
			logger.info('Target completed: SHORT: %f : %s'%(ltp, bucket))
			bucket = self.completed(ltp,bucket)
		elif trend == "long" and ltp <= stoploss:
			logger.info('Stoploss completed: LONG: %f : %s'%(ltp, bucket))
			bucket = self.stoploss('LONG', ltp, bucket)
		elif trend == "short" and ltp >= stoploss:
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
					instrm = bucket["id"].split(":")
					name = self.__spread_info[instrm[4]]["symbol"] if instrm[4] in self.__spread_info else instrm[4]
					self.invoke_bot_message('SIGNAL (BUY): %s : %s min : entry : %f : status : %s'%(name, duration, bucket["entry"], bucket["status"]))
				elif "short" == bucket["trend"] and float(cdata["low"]) < float(bucket["low"]) and float(cdata["macd"]) < 0 and status != "SIGNAL":
					bucket["entry"] = float(cdata["low"]) - entry_spread
					bucket["status"] = "SIGNAL"
					instrm = bucket["id"].split(":")
					name = self.__spread_info[instrm[4]]["symbol"] if instrm[4] in self.__spread_info else instrm[4]
					self.invoke_bot_message('SIGNAL (SELL): %s : %s min : entry : %f : status : %s'%(name, duration, bucket["entry"], bucket["status"]))
				elif ("long" == bucket["trend"] and float(cdata["macd"]) < 0) or ("short" == bucket["trend"] and float(cdata["macd"]) > 0):
					bucket = self.invalidate(bucket)
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
						# instrm = bucket["id"].split(":")
						# name = self.__spread_info[instrm[4]]["symbol"] if instrm[4] in self.__spread_info else instrm[4]
						# self.invoke_bot_message('SIGNAL: %s : trend %s : %s min : high : %s : low : %s'%(name, bucket["trend"], duration, bucket["high"], bucket["low"]))
					return bucket
			else:
				macd = float(cdata["macd"]) if "macd" in cdata else 0
				if "long" == bucket["trend"] and macd < 0:
					bucket["stoploss"] = float(cdata["low"]) - entry_spread
					# self.invoke_bot_message('SIGNAL|PREPARE|LONG|%s'%bucket)
				elif "short" == bucket["trend"] and macd > 0:
					bucket["stoploss"] = float(cdata["high"]) + entry_spread
					# self.invoke_bot_message('SIGNAL|PREPARE|SHORT|%s'%bucket)
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
				# logger.info('Freshly checking after invalidate %s'%bucket)
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
					# instrm = bucket["id"].split(":")
					# name = self.__spread_info[instrm[4]]["symbol"] if instrm[4] in self.__spread_info else instrm[4]
					# self.invoke_bot_message('SIGNAL: %s : trend %s : %s min : high : %s : low : %s'%(name, bucket["trend"], duration, bucket["high"], bucket["low"]))
					return find_buffer(cdata, pdata, bucket)
			else:
				return find_buffer(cdata, pdata, bucket)
			return bucket
		return find_trend(curr_data, prev_data, bucket)
MACDStrategy()




















