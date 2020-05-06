import requests
import csv
from modules.props.ConfigProps import AppProperties, AppLogger

logger = AppLogger()

class Nifty50():
	def fetchNifty50(self):
		nifty50_list = list([])
		with requests.Session() as csv_session:
			nifty50_csv = csv_session.get(AppProperties['NIFTY50_URL'])
			decoded_content = nifty50_csv.content.decode('utf-8')
			cr = csv.reader(decoded_content.splitlines(), delimiter=',')
			next(cr)
			nifty50_list = list(cr)
			nifty50_instruments = list([])
			for equity in nifty50_list:
				nifty50_instruments.append(equity[2])
				logger.debug('Instrument fetched: %s'%(equity[2]))
		return nifty50_instruments