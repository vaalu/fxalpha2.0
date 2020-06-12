import json
from modules.props.ConfigProps import AppOHLCLogger

logger = AppOHLCLogger('OHLCItemProcessor')
class OHLCItemProcessor():
	__in_mem={
		"instrument":"",
		"open":0.0, 
		"high":0.0, 
		"low":0.0,
		"close":0.0,
		"timestamp":0, 
		"isotimestamp":""
	}
	
	def __init__(self):
		logger.debug('Initializing OHLC Processing')
	
	def __init__(self, instr_key):
		logger.debug('Initializing OHLC Processing for %s'%(instr_key))
	
	def __default_callback(self, arg):
		logger.debug(args)

	def process_ohlc(self, data, callback=__default_callback):
		if callback != None:
			callback(data)

	def find_low(self, curr:0.0, upd:0.0):
		return curr if curr==upd else curr if curr < upd else upd
	
	def find_high(self, curr:0.0, upd:0.0):
		return curr if curr==upd else curr if curr > upd else upd

	def calculate_ohlc(self, instrument_token, spec_duration, timestamp, json_data):
		logger.info('Processing for %s:%i'%(instrument_token, timestamp))
		ts_key = '%s:%s'%(instrument_token, spec_duration)
		if ts_key == self.__in_mem["instrument"]:
			self.__in_mem["high"] = self.find_high(float(self.__in_mem["high"]), float(json_data["high"]))
			self.__in_mem["low"] = self.find_low(float(self.__in_mem["low"]), float(json_data["low"]))
		else:
			self.__in_mem["instrument"] = ts_key
			self.__in_mem["instrument_key"] = instrument_token
			self.__in_mem["open"] = float(json_data["open"])
			self.__in_mem["high"] = float(json_data["high"])
			self.__in_mem["low"] = float(json_data["low"])
		self.__in_mem["close"] = float(json_data["close"])
		self.__in_mem["timestamp"] = timestamp
	def final_save(self, callback):
		self.process_ohlc(self.__in_mem, callback)
		logger.info(self.__in_mem)

