import csv
import requests
from datetime import datetime, timedelta
from modules.AliceUtil import AliceUtil
from modules.props.ConfigProps import AppLogger, AppProps
from alice_blue import *
import pandas as pd

logger = AppLogger('AliceInstruments')

class AliceInstruments():
	access_token = AliceUtil.get_instance().fetchTokenIfNotExists()
	try:
		alice = AliceBlue(	username=AppProps['CLIENT_USER'], 
							password=AppProps['CLIENT_PASSWORD'], 
							access_token=access_token, 
							master_contracts_to_download=['NSE', 'MCX'])
	except:
		logger.debug('Unable to fetch token. Abandoning further requests.')
	__month_arr = ["", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
	def __init__(self):
		logger.debug('Initializing Alice instruments')
	def current_month(self):
		logger.info('Calculating current month')
		today = datetime.today()
		return [today, today.year, today.month, today.day, self.__month_arr[today.month]]
	def calculate_date_early_by_2_days(self, curr_date, instr, symbol, symbol_id ):
		expiry_calc = curr_date + timedelta(days=2)
		date_args = instr.expiry.timetuple()[:6]
		expiry_datetime = datetime(*date_args)
		mon_str = self.__month_arr[curr_date.month]
		instr_symbol = instr.symbol
		if expiry_calc > expiry_datetime:
			mon_str = self.__month_arr[curr_date.month + 1]
			logger.info('Instrument FutCom %s expiring soon. Hence changing date from %s to %s'%(instr.symbol, expiry_calc, mon_str))
			instr_symbol = '%s %s FUT'%(symbol, mon_str)
		logger.info('Expiry symbol: %s'%instr_symbol)
		return instr_symbol
	def process_csv_content(self, nifty50_list):
		nifty50_instruments = []
		consolidated_nifty_50_securities = []
		for equity in nifty50_list:
			instr = self.alice.get_instrument_by_symbol(exchange='NSE', symbol=equity[2])
			consolidated_nifty_50_securities.append(instr)
			nifty50_instruments.append([1, instr.token])
		return nifty50_instruments, consolidated_nifty_50_securities
	def fetchNifty50(self):
		nifty50_list = list([])
		nifty_50_url = AppProps['NIFTY50_URL']
		nifty_50_file = AppProps['NIFTY50_FILE']
		# Download CSV file from Nifty50. If unable to download, then fallback to existing nifty50 file.
		try:
			csv_df = pd.read_csv(nifty_50_url)
			csv_df.head()
			csv_df.to_csv(nifty_50_file, index=False)
		except OSError as err:
			logger.error('Unable to fetch Nifty50. Hence fallback to existing file: %s'%err)
		with open(nifty_50_file, 'r') as csv_file:
			reader = csv.reader(csv_file)
			next(reader)
			for row in reader:
				nifty50_list.append(row)
		return self.process_csv_content(nifty50_list)
	def fetch_commodities(self):
		logger.info('Fetching required commodities')
		selected_commodities = AppProps['COMMODITIES_MCX']
		logger.info(selected_commodities)
		[today, year, month, day, month_str] = self.current_month()
		logger.info('Year %i - %i - %i - %s'%(year, month, day, month_str))
		commodities_list = list([])
		commodities_token_list = list([])
		for commodity in selected_commodities:
			symbol_id = '%s %s FUT'%(commodity, month_str)
			instr = self.alice.get_instrument_by_symbol(exchange='MCX', symbol=symbol_id)
			if instr == None:
				new_month_str = self.__month_arr[month + 1]
				symbol_id = '%s %s FUT'%(commodity, new_month_str)
				instr = self.alice.get_instrument_by_symbol(exchange='MCX', symbol=symbol_id)
			processed_sym = self.calculate_date_early_by_2_days(today, instr, commodity, symbol_id)
			logger.info('Processed symbol %s vs actual %s'%(processed_sym, symbol_id))
			if processed_sym != symbol_id:
				instr = self.alice.get_instrument_by_symbol(exchange='MCX', symbol=processed_sym)
			mth_indx = month
			while instr == None:
				mth_indx = mth_indx + 1 if mth_indx < 12 else 1
				new_month_str = self.__month_arr[mth_indx]
				symbol_id = '%s %s FUT'%(commodity, new_month_str)
				instr = self.alice.get_instrument_by_symbol(exchange='MCX', symbol=symbol_id)
			commodities_list.append(instr)
			commodities_token_list.append([4, instr.token])
		logger.info('Fetching for commodities %s'%str(commodities_list))
		return commodities_list, commodities_token_list