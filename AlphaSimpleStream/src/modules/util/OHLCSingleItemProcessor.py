import json
from modules.props.ConfigProps import AppLogger

logger = AppLogger()
class OHLCSingleItemProcessor():
	__in_mem={}
	
	def __init__(self):
		logger.info('Initializing OHLC Processing')
	
	def __default_callback(self, arg):
		logger.debug(args)

	def process_ohlc(self, data, callback=__default_callback):
		if callback != None:
			callback(data)

	def find_low(self, curr:0.0, upd:0.0):
		return curr if curr==upd else curr if curr < upd else upd
	
	def find_high(self, curr:0.0, upd:0.0):
		return curr if curr==upd else curr if curr > upd else upd

	def calculate_ohlc(self, instrument_token, exch_timestamp, json_data, callback=__default_callback):
		# Initialize cache
		previous_key = str(exch_timestamp -1)
		ts_key = str(exch_timestamp)
		instr = str(instrument_token)
		ohlc_key = "1s:ohlc"
		if ts_key in self.__in_mem:
			if instr in self.__in_mem[ts_key]:
				existing_data = self.__in_mem[ts_key]
				existing_data["actual"].append(json_data)
				existing_data[ohlc_key]["high"] = self.find_high(existing_data[ohlc_key]["high"], json_data["last_traded_price"])
				existing_data[ohlc_key]["low"] = self.find_low(existing_data[ohlc_key]["low"], json_data["last_traded_price"])
				existing_data[ohlc_key]["close"]=json_data["last_traded_price"]
			else:
				self.__in_mem[ts_key] = {}
				self.__in_mem[ts_key]["actual"] = []
				self.__in_mem[ts_key]["actual"].append(json_data)
				self.__in_mem[ts_key][ohlc_key] = {
					"instrument":'%s:%s'%(instr, ts_key), 
					"open":json_data["last_traded_price"],
					"high":json_data["last_traded_price"],
					"low":json_data["last_traded_price"],
					"close":json_data["last_traded_price"], 
					"timestamp":exch_timestamp 
				}
			self.__in_mem["existing"]=self.__in_mem[ts_key]
		else:
			if "existing" in self.__in_mem:
				self.process_ohlc(self.__in_mem["existing"][ohlc_key], callback=callback)
				try:
					self.__in_mem.pop("existing")
				except KeyError:
					print("Key 'existing' not found")
			self.__in_mem[ts_key] = {}
			self.__in_mem[ts_key] = {}
			self.__in_mem[ts_key]["actual"] = []
			self.__in_mem[ts_key]["actual"].append(json_data)
			self.__in_mem[ts_key][ohlc_key] = {
				"instrument":'%s:%s'%(instr, ts_key), 
				"open":json_data["last_traded_price"],
				"high":json_data["last_traded_price"],
				"low":json_data["last_traded_price"],
				"close":json_data["last_traded_price"], 
				"timestamp":exch_timestamp
			}
			self.__in_mem["existing"]=self.__in_mem[ts_key]