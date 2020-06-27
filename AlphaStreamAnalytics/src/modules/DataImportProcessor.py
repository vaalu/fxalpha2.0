import os
import json
import ast
from modules.util.RedisUtil import RedisUtil
from modules.util.RedisCalcUtil import RedisCalcUtil
from modules.props.ConfigProps import AppDataBackupLogger, AppProps

logger = AppDataBackupLogger.get_instance()

class DataImportProcessor():
	__redis_util = RedisCalcUtil()
	__red = RedisUtil.get_instance()
	__equities, __commodities, __all_instruments = __red.fetch_all_instruments()
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
		for instrument in self.__all_instruments:
			token = instrument["token"]
			symbol = instrument["symbol"]
			logger.info('Instrument %s : %s'%(token, symbol))
			data = self.read_prev_from_file(token, symbol, 1)
			self.__redis_util.save_imported(data)
			data = self.read_from_file(token, symbol, 5)
			self.__redis_util.save_imported(data)


