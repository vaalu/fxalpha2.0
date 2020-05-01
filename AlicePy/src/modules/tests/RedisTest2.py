import redis
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

r = redis.Redis(host='localhost', port=6379)

props = aliceAnt

print('Testing ...')

# producer = KafkaProducer(bootstrap_servers='localhost:9092')
# producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def test1():
	interval = '5min'
	symbol = 'IBM'
	alphavantage_url = '%s/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=%s&outputsize=full&apikey=%s'%(props['ALPHAVANTAGE_URL'], symbol, interval, props['ALPHAVANTAGE_KEY'])
	print(alphavantage_url)

	req = urllib.request.urlopen(alphavantage_url)
	data = req.read()
	json_obj = json.loads(data)
	series_data = list([])
	queue = Queue()
	for key in json_obj.keys():
		print(key)
		if 'Time Series' in key:
			tick = json_obj[key]
			tick_keys = tick.keys()
			for tick_key in tick_keys:
				r.hset(tick_key, tick_key, tick_key)
				r.hset(tick_key, "instrument_token","ibm")
				r.hset(tick_key, "last_traded_price", tick[tick_key]["4. close"])
				r.hset(tick_key, "last_traded_time", tick_key)
				r.hset(tick_key, "trade_volume", tick[tick_key]["5. volume"])
				r.hset(tick_key, "exchange_timestamp", tick_key) 
				r.hset(tick_key, "open_price", tick[tick_key]["1. open"])
				r.hset(tick_key, "high_price", tick[tick_key]["2. high"])
				r.hset(tick_key, "low_price", tick[tick_key]["3. low"])
				r.hset(tick_key, "close_price", tick[tick_key]["4. close"])
				r.hset(tick_key, "yearly_high_price", tick[tick_key]["2. high"])
				r.hset(tick_key, "yearly_low_price", tick[tick_key]["2. high"])
				print('Posted %s'%(tick_key))
			print('Completed posting data to solr server')
	queue.join()
# red.hgetall('ibm:*')
test1()
