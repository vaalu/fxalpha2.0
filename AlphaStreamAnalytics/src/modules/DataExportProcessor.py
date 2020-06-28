import os
import json
from modules.props.ConfigProps import AppProps, AppDataBackupLogger
from modules.util.DateTimeUtil import DateTimeUtil
from modules.util.RedisUtil import RedisUtil
from modules.util.RedisCalcUtil import RedisCalcUtil

logger = AppDataBackupLogger.get_instance()

class DataExportProcessor():
	__date_util = DateTimeUtil.get_instance()
	__red_util = RedisUtil.get_instance()
	__red_calc_util = RedisCalcUtil()
	def __init__(self):
		logger.info('Initializing data export')
	def split_as_batch(self, iterable, batch_size):
		for indx in range(0, len(iterable), batch_size):
			yield iterable[indx:indx + batch_size]
	def write_to_file(self, instr_token, instr_name, duration, data) :
		backup_path = '%s/data'%AppProps["LOG_DIR"]
		try:
			os.makedirs(backup_path)
		except OSError as e:
			pass
		try:
			bkp_file = ('%s/%s-%s-%i-min.data.json'%(backup_path, instr_token, instr_name, duration)).replace(" ", "-")
			logger.info('Writing data for: %s'%instr_name)
			with open(bkp_file, 'w') as file:
				json.dump(data, file)
				file.close()
		except:
			logger.info('Unable to create backup file')
	def prepare_data(self, instruments, duration):
		start_time, end_equities, end_commodities = self.__date_util.get_market_timings()
		for instrument in instruments:
			instr_token = instrument["token"]
			instr_name = instrument["symbol"]
			logger.info('Collecting %i min ohlc data for %s : %s'%(duration, instr_token, instr_name))
			init_time = start_time
			calc_min = 60 * duration
			data_keys = []
			data = list([])
			while init_time < end_commodities:
				init_time += calc_min
				data_keys.append('%s:%iM:%i'%(instr_token, duration, init_time))
			split_keys = self.split_as_batch(data_keys, int(60/duration))
			for batch_keys in split_keys:
				data.extend(self.__red_calc_util.fetch_data(instr_token, batch_keys))
			self.write_to_file(instr_token, instr_name, duration, data)
	def backup(self):
		instruments = []
		instruments.extend(self.__red_util.fetch_processing_instruments("EQUITY"))
		instruments.extend(self.__red_util.fetch_processing_instruments("COMMODITY"))
		self.prepare_data(instruments, 1)
		self.prepare_data(instruments, 5)
		
