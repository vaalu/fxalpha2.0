#!/usr/bin/env python3
import csv
import requests
import configparser
import logging 
from modules.props.ConfigProps import AppLogger

config = configparser.ConfigParser()
config.read('application.config.properties')

exchange_code_equities=int(config.get('TRADING_INSTRUMENTS', 'exchange.code.equity'))

logger = AppLogger()

class EquitiesData():
	def __init__(self):
		logger.info('Nifty 50 equities instrument data to be consolidated')
	
	@classmethod
	def fetchCollectedEquities(self, collected_csv):
		static_list = list([])
		with open(collected_csv, newline='') as equity_csv:
			csv_reader = csv.reader(equity_csv, delimiter=',')
			static_list = list(csv_reader)
		return static_list
	
	@classmethod
	def fetchNifty50(self, collected_csv, nifty50_path):
		nifty50_list = list([])
		static_list = self.fetchCollectedEquities(collected_csv)
		with requests.Session() as csv_session:
			nifty50_csv = csv_session.get(nifty50_path)
			decoded_content = nifty50_csv.content.decode('utf-8')
			cr = csv.reader(decoded_content.splitlines(), delimiter=',')
			nifty50_list = list(cr)
			consolidated_nifty_50_securities = []
			for equity in nifty50_list:
				selected_instrument = next((instrument for instrument in static_list if instrument[2] == equity[2] and instrument[10] == 'NSE'), None)
				if selected_instrument is not None: 
					consolidated_nifty_50_securities.append([exchange_code_equities, int(selected_instrument[1])])
			return consolidated_nifty_50_securities

if __name__ == "__main__":
	sec = EquitiesData().fetchNifty50('./equities.csv', 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv')
	print(sec)
