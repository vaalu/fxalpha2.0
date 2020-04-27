import urllib.request
import json
from modules.props.ConfigProps import aliceAnt
from datetime import datetime
import pysolr
from queue import Queue
from threading import Thread

try:
	import thread
except ImportError:
	import _thread as thread
import time

props = aliceAnt

print('Testing ...')
solr = pysolr.Solr('http://mohu.local:8983/solr/test', always_commit=True)
solr.ping()

class DownloadWorker(Thread):
	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue
	def run(self):
		while True:
			solr_post = self.queue.get()
			try:
				solr.add([solr_post])
			finally:
				self.queue.task_done()
def test1():
	# print(props)
	interval = '5min'
	symbol = 'IBM'
	# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=DPS&interval=5min&outputsize=full&apikey=5U19TJGGJJNLYEIR
	alphavantage_url = '%s/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=%s&outputsize=full&apikey=%s'%(props['ALPHAVANTAGE_URL'], symbol, interval, props['ALPHAVANTAGE_KEY'])
	print(alphavantage_url)

	req = urllib.request.urlopen(alphavantage_url)
	data = req.read()
	json_obj = json.loads(data)
	# print (json_obj.keys())
	series_data = list([])
	queue = Queue()
	for key in json_obj.keys():
		print(key)
		if 'Time Series' in key:
			# print (json_obj[key])
			tick = json_obj[key]
			tick_keys = tick.keys()
			# print (tick_keys)
			for tick_key in tick_keys:
				tick_obj = {
					"instrument_token":"ibm",
					"last_traded_price": tick[tick_key]["4. close"],
					"last_traded_time": tick_key, 
					"trade_volume": tick[tick_key]["5. volume"],
					"exchange_timestamp": tick_key, 
					"open_price": tick[tick_key]["1. open"],
					"high_price": tick[tick_key]["2. high"],
					"low_price": tick[tick_key]["3. low"],
					"close_price": tick[tick_key]["4. close"],
					"yearly_high_price": tick[tick_key]["2. high"],
					"yearly_low_price": tick[tick_key]["2. high"]
				}
				worker = DownloadWorker(queue)
				worker.daemon = True
				worker.start()
				queue.put(tick_obj)
				# def postToSolr(*args):
				#	solr.add([tick_obj])
				#	print('Posted tick obj datum... ')
				# thread.start_new_thread(postToSolr, ())
				# series_data.append(tick_obj)
			print('Completed posting data to solr server')
	queue.join()
	# print('Data obtained %s', json.loads(data))
	# dt = datetime.fromtimestamp(1587735863)
	# print(dt)
	# val = {"2020-04-03 09:55:00": {"1. open": "109.3900", "2. high": "109.5700", "3. low": "109.1100", "4. close": "109.5700", "5. volume": "43358" }}
	# print(json_obj)

test1()
