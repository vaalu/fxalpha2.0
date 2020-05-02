import json
import csv
import requests
import configparser
import datetime
from alice_blue import *
from modules.AliceUtil import AliceUtil
from modules.props.ConfigProps import aliceAnt

print('Fetching access token from alice blue ant API')
config = configparser.ConfigParser()
config.read('application.config.properties')

class AliceInstruments():
	instrument_names=aliceAnt['COMMODITIES_MCX']
	access_token = AliceUtil().fetchTokenIfNotExists()
	try:
		alice = AliceBlue(	username=aliceAnt['CLIENT_USER'], 
							password=aliceAnt['CLIENT_PASSWORD'], 
							access_token=access_token, 
							master_contracts_to_download=['NSE', 'MCX'])
	except:
		print('Unable to fetch token. Abandoning further requests.')

	def __init__(self):
		print('Alice API access:')
		print('Alice token %s'%(self.access_token))
	
	def __futures_date(self):
		print('Checking date validity of instruments')

	def getCommodityInstruments(self):
		print('Fetching commodity instruments')
		commodities_instr = list([])
		# print(self.alice.search_instruments('MCX', 'GOLD'))
		for instr in self.instrument_names:
			instr_obj = self.alice.get_instrument_by_symbol(exchange='MCX', symbol=('%s MAY FUT'%(instr)))
			commodities_instr.append(instr_obj)
		print(commodities_instr)
		# commodities_instr.append([4, instr])
		# return commodities_instr


if __name__ == "__main__":
	alice = AliceInstruments().getCommodityInstruments()