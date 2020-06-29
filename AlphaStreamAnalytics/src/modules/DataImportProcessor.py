import os
import json
import ast
from modules.util.RedisUtil import RedisUtil
from modules.util.RedisCalcUtil import RedisCalcUtil
from modules.util.DateTimeUtil import DateTimeUtil
from modules.props.ConfigProps import AppDataBackupLogger, AppProps

logger = AppDataBackupLogger.get_instance()

class DataImportProcessor():
	__redis_util = RedisCalcUtil()
	__red = RedisUtil.get_instance()
	__equities, __commodities, __all_instruments = __red.fetch_all_instruments()
	__date_util = DateTimeUtil.get_instance()
	def __init__(self):
		logger.info('Processing import processor')
	def read_from_file(self, instr_token, instr_name, duration) :
		backup_path = '%s/data'%AppProps["LOG_DIR"]
		data = []
		try:
			os.makedirs(backup_path)
		except OSError as e:
			pass
		try:
			bkp_file = ('%s/%s-%s-%i-min.data.json'%(backup_path, instr_token, instr_name, duration)).replace(" ", "-")
			logger.info('Reading data from file %s'%bkp_file)
			with open(bkp_file, 'r') as file:
				data = json.load(file)
		except OSError as e:
			logger.info('Unable to read backup file %s'%e)
		return data
	def read_prev_from_file(self, instr_token, instr_name, duration) :
		backup_path = '%s/data.1'%AppProps["LOG_DIR"]
		data = []
		try:
			os.makedirs(backup_path)
		except OSError as e:
			pass
		try:
			bkp_file = ('%s/%s-%s-%i-min.data.json'%(backup_path, instr_token, instr_name, duration)).replace(" ", "-")
			logger.info('Reading data from file %s'%bkp_file)
			with open(bkp_file, 'r') as file:
				data = json.load(file)
		except OSError as e:
			logger.info('Unable to read backup file %s'%e)
		return data
	def read_data_from_backup(self):
		for instrument in self.__all_instruments:
			token = instrument["token"]
			symbol = instrument["symbol"]
			logger.info('Instrument %s : %s'%(token, symbol))
			data = self.read_from_file(token, symbol, 1)
			self.__redis_util.save_imported(data)
			data = self.read_from_file(token, symbol, 5)
			self.__redis_util.save_imported(data)
	def read_prev_data_from_backup(self):
		start_time, eq_time, cm_time = self.__date_util.get_market_timings_previous_day()
		def last_30_values(instrument, data, duration):
			if data != None:
				items_to_save = []
				total_items = 30
				prev_items = data[-total_items:]
				init_time = start_time - (30 * (60 * duration))
				for index in range(0, 31):
					time_key = init_time + (index * (60 * duration))
					token = instrument["token"]
					key = "%s:%iM:%s"%(token, duration, int(time_key))
					item = data[index]
					item["instrument"] = key
					# logger.info('Substituted key: %s | %s'%(key, item ))
					items_to_save.append(item)
				if items_to_save != None and len(items_to_save) > 0:
					self.__redis_util.save_imported(items_to_save)
		for instrument in self.__equities:
			token = instrument["token"]
			symbol = instrument["symbol"]
			logger.info('Instrument %s : %s'%(token, symbol))
			data = self.read_prev_from_file(token, symbol, 1)
			last_30_values(instrument, data, 1)
			data = self.read_prev_from_file(token, symbol, 5)
			last_30_values(instrument, data, 5)


