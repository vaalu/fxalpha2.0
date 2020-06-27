from modules.props.ConfigProps import AppStrategyLogger
from modules.util.RedisStrategyUtil import RedisStrategyUtil

logger = AppStrategyLogger('MACDStrategyLegacy')
class MACDStrategyLegacy():
	__red_stg_util = RedisStrategyUtil()
	__strategy_id = 'MACD'
	__store = {}
	__name = "MACD"
	__instance = None
	__lifecycle : {
		"TREND_SIGNAL":{}, 	# Determine long or short macd neg to pos = long; macd pos to neg = short
		"BUFFER_SIGNAL":{},	# if long, macd pos and curr_high > trend_signal_high, entry = curr_high + entry_spread
		"ENTRY":{},			# if long, macd pos and curr_high > buffer_high status = enter and target = target_spread
		"INVALIDATE":{},
		"STOPLOSS":{}		# if long, macd neg, set sl
		"TARGET":{}			# if long curr_high > target_spread status = "COMPLETE"
	}
	@staticmethod
	def get_instance():
		if MACDStrategyLegacy.__instance == None:
			MACDStrategyLegacy()
		return MACDStrategyLegacy.__instance
	def __init__(self):
		print('MACD Strategy')
		if MACDStrategyLegacy.__instance != None:
			raise Exception('MACD Strategy is now singleton')
		else:
			MACDStrategyLegacy.__instance = self
	def get_name(self):
		return self.__name
	def reset_bucket(self, bucket):
		self.__red_stg_util.reset(bucket)
		logger.info('INVALIDATED|%s'%(bucket))
	def invoke_cover(self, instr, cover_trend, curr_macd, prev_macd, ltp, trigger_price):
		logger.info('COVER|%s|%s|%f|%f|%f|%f'%(cover_trend, instr, curr_macd, prev_macd, ltp, trigger_price))
	def invoke_stoploss(self, instr, sl_trend, ltp, trigger_price):
		logger.info('SL|%s|%s|%f|%f'%(sl_trend, instr, ltp, trigger_price))
	def invoke_buy(self, instr, ltp, trigger_price):
		logger.info('LONG|ENTRY|%s|%f|%f'%(instr, ltp, trigger_price))
	def invoke_sell(self, instr, ltp, trigger_price):
		logger.info('SHORT|ENTRY|%s|%f|%f'%(instr, ltp, trigger_price))
	def invoke_long_cover(self, instr, ltp, target_price):
		logger.info('LONG|COVER|%s|%f|%f'%(instr, ltp, target_price))
	def invoke_short_cover(self, instr, ltp, target_price):
		logger.info('SHORT|COVER|%s|%f|%f'%(instr, ltp, target_price))
	def process(self, data):
		instr = data["instrument_token"]
		bucket_01, bucket_05 = self.__red_stg_util.fetch_strategies(self.__name, instr)
		buckets = [bucket_01, bucket_05]
		for bucket in buckets:
			trend = bucket["trend"] if "trend" in bucket else ""
			ltp = float(data["last_traded_price"])
			duration = 1 if bucket == bucket_01 else 5
			if "entry" in bucket and "status" in bucket and bucket["status"] == "ENTRY":
				entry_price = float(bucket["entry"])
				stoploss = float(bucket["stoploss"]) if "stoploss" in bucket else 0
				if trend == "long" and ltp > entry_price:
					self.invoke_buy(instr, ltp, entry_price)
					bucket["status"] == "RUNNING"
				elif trend == "short" and ltp < entry_price:
					self.invoke_sell(instr, ltp, entry_price)
					bucket["status"] == "RUNNING"
				elif trend == "long" and ltp < stoploss:
					self.invoke_stoploss(instr, "SL_LONG", ltp, stoploss)
					bucket["status"] = "invalidated"
					bucket["sl_trigger"] = ""
					bucket["trend"] = "invalidated"
					bucket["stoploss"] = 0
				elif trend == "short" and ltp > stoploss:
					self.invoke_stoploss(instr, "SL_SHORT", ltp, stoploss)
					bucket["status"] = "invalidated"
					bucket["sl_trigger"] = ""
					bucket["trend"] = "invalidated"
					bucket["stoploss"] = 0 
			elif "status" in bucket and bucket["status"] == "RUNNING":
				if trend == "long" and ltp >= float(bucket["target"]):
					self.invoke_long_cover(instr, ltp, float(bucket["target"]))
					bucket["status"] = "invalidated" 
					bucket["trend"] = "invalidated"
					bucket["stoploss"] = 0 
				elif trend == "short" and ltp <= float(bucket["target"]):
					self.invoke_short_cover(instr, ltp, float(bucket["target"]))
					bucket["status"] = "invalidated"
					bucket["trend"] = "invalidated"
					bucket["stoploss"] = 0 
			self.__red_stg_util.save_strategy(self.__name, instr, duration, bucket) 
	def analyze(self, instr, duration, curr_data, prev_data, entry_spread, target_spread, bucket):
		if curr_data != None and curr_data != {} and prev_data != None and prev_data != {}:
			curr_macd = float(curr_data["macd"]) if curr_data != None and "macd" in curr_data else 0
			prev_macd = float(prev_data["macd"]) if prev_data != None and "macd" in prev_data else 0
			if "trend" not in bucket or bucket["trend"] == "invalidated":
				if curr_macd > 0 and prev_macd < 0:
					bucket["trend"] = "long"
					logger.info('LONG|INIT|%s|%s|%s|%s'%(curr_data["instrument"], prev_data["instrument"], curr_data["macd"], prev_data["macd"]))
				elif curr_macd < 0 and prev_macd > 0:
					bucket["trend"] = "short"
					logger.info('SHORT|INIT|%s|%s|%s|%s'%(curr_data["instrument"], prev_data["instrument"], curr_data["macd"], prev_data["macd"]))
				if "trend" in bucket and bucket["trend"] != "invalidated":
					bucket["high"] = float(curr_data["high"])
					bucket["low"] = float(curr_data["low"])
					bucket["macd"] = float(curr_data["macd"])
			else:
				if curr_data != None and curr_data != {}:
					bucket_high = float(bucket["high"]) if "high" in bucket else 0
					curr_high = float(curr_data["high"])
					bucket_low = float(bucket["low"]) if "low" in bucket else 0
					curr_low = float(curr_data["low"]) 
					bucket_macd = float(bucket["macd"]) if "macd" in bucket else 0
					curr_macd = float(curr_data["macd"])
					is_applied = bucket["is_applied"] if "is_applied" in bucket else "no"
					curr_trend = bucket["trend"] if "trend" in bucket else ""
					status = bucket["status"] if "status" in bucket else ""
					if (curr_trend == "long" and curr_macd < 0) or (curr_trend == "short" and curr_macd > 0):
						logger.info('2. Invalidated: Instr:%s|trend:%s|cmacd:%f|pmacd:%f|bstatus:%s'%(instr, curr_trend, curr_macd, prev_macd, status))
						bucket["status"] = "invalidated"
						bucket["trend"] = "invalidated"
						self.reset_bucket(bucket)
					if status == "ENTRY":
						if curr_trend == "long" and "target" in bucket and curr_high >= float(bucket["target"]):
							bucket["status"] = "invalidated"
							logger.info('1. long cover :%s|trend:%s|high:%f|low:%f|cmacd:%f|pmacd%f|%s'%(instr, curr_trend, curr_high, curr_low, curr_macd, prev_macd, status))
							self.invoke_cover(isntr, "BUY", curr_macd, prev_macd, curr_high, float(bucket["target"]))
						elif curr_trend == "short" and "target" in bucket and curr_low <= float(bucket["target"]):
							bucket["status"] = "invalidated"
							logger.info('1. short cover :%s|trend:%s|high:%f|low:%f|cmacd:%f|pmacd%f|%s'%(instr, curr_trend, curr_high, curr_low, curr_macd, prev_macd, status))
							self.invoke_cover(isntr, "SELL", curr_macd, prev_macd, curr_low, float(bucket["target"]))
						elif curr_trend == "long" and curr_macd < 0 and ("sl_trigger" not in bucket or bucket["sl_trigger"] == ""):
							bucket["stoploss"] = curr_low - entry_spread
							bucket["sl_trigger"] = "yes"
							logger.info('1. long set SL :%s|trend:%s|high:%f|low:%f|cmacd:%f|pmacd%f|SL:%s|%s'%(instr, curr_trend, curr_high, curr_low, curr_macd, prev_macd, bucket["stoploss"], status))
						elif curr_trend == "long" and curr_macd > 0 and "sl_trigger" in bucket:
							bucket["stoploss"] = 0
							bucket["sl_trigger"] = "no"
						elif curr_trend == "short" and curr_macd > 0 and ("sl_trigger" not in bucket or bucket["sl_trigger"] == ""):
							bucket["stoploss"] = curr_high + entry_spread
							bucket["sl_trigger"] = "yes"
							logger.info('1. short set SL :%s|trend:%s|high:%f|low:%f|cmacd:%f|pmacd%f|SL:%f|%s'%(instr, curr_trend, curr_high, curr_low, curr_macd, prev_macd, bucket["stoploss"], status))
						elif curr_trend == "short" and curr_macd < 0 and "sl_trigger" in bucket:
							bucket["stoploss"] = 0
							bucket["sl_trigger"] = "no"
					elif (curr_trend == "long" and curr_macd < 0) or (curr_trend == "short" and curr_macd > 0):
						logger.info('2. Invalidated: Instr:%s|trend:%s|cmacd:%f|pmacd:%f|bstatus:%s'%(instr, curr_trend, curr_macd, prev_macd, status))
						bucket["status"] = "invalidated"
						bucket["trend"] = "invalidated"
						self.reset_bucket(bucket)
					elif bucket["trend"] == "long" and curr_macd > 0 and bucket["trend"] != "RUNNING":
						bucket["entry"] = curr_high + entry_spread
						bucket["status"] = "ENTRY"
						logger.info('3. Entry: Instr:%s|trend:%s|cmacd:%f|entry:%f|bstatus:%s'%(instr, curr_trend, curr_macd, bucket["entry"], status))
					elif bucket["trend"] == "short" and curr_macd < 0 and bucket["trend"] != "RUNNING":
						bucket["entry"] = curr_low - entry_spread
						bucket["status"] = "ENTRY"
						logger.info('4. Entry: Instr:%s|trend:%s|cmacd:%f|entry:%f|bstatus:%s'%(instr, curr_trend, curr_macd, bucket["entry"], status))
			self.__red_stg_util.save_strategy(self.__name, instr, duration, bucket)
MACDStrategyLegacy()
			










