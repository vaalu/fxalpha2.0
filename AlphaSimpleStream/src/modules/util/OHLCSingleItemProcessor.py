import json
import datetime
from modules.props.ConfigProps import AppLogger

logger = AppLogger()
class OHLCSingleItemProcessor():
	__in_mem={
		"instrument":"",
		"open":0.0, 
		"high":0.0, 
		"low":0.0,
		"close":0.0,
		"timestamp":0, 
		"isotimestamp":"",
		"data_actuals":[]
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

	def calculate_ohlc(self, instrument_token, spec_duration, exch_timestamp, json_data):
		# print('Processing for %i:%i'%(instrument_token, exch_timestamp))
		# print(json_data)
		ts_key = '%i:%s'%(instrument_token, spec_duration)
		if ts_key == self.__in_mem["instrument"]:
			self.__in_mem["high"] = self.find_high(float(self.__in_mem["high"]), float(json_data["last_traded_price"]))
			self.__in_mem["low"] = self.find_low(float(self.__in_mem["low"]), float(json_data["last_traded_price"]))
		else:
			self.__in_mem["instrument"] = ts_key
			self.__in_mem["open"] = float(json_data["last_traded_price"])
			self.__in_mem["high"] = float(json_data["last_traded_price"])
			self.__in_mem["low"] = float(json_data["last_traded_price"])
			self.__in_mem["timestamp"] = exch_timestamp
			self.__in_mem["isotimestamp"] = datetime.datetime.fromtimestamp(exch_timestamp).isoformat() 
		self.__in_mem["close"] = float(json_data["last_traded_price"])
		self.__in_mem["data_actuals"].append(json_data)
	def final_save(self, callback):
		self.process_ohlc(self.__in_mem, callback)
		print(self.__in_mem)

