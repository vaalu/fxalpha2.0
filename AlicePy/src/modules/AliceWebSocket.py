#!/usr/bin/env python3
from modules.MarketData import CliMarketdataRes
import websocket
import json
from kafka import KafkaProducer
import urllib 
from modules.props.ConfigProps import aliceAnt, AppLogger

logger = AppLogger()

kafka_server = '%s:%s'%(aliceAnt['KAFKA_URL'], aliceAnt['KAFKA_PORT'])
producer = KafkaProducer(bootstrap_servers=kafka_server, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

try:
	import thread
except ImportError:
	import _thread as thread
import time
multiplier = {
	'1':100,
	'2':100,
	'3':10000000,
	'4':100,
	'6':100,
	'7':100
}
multiplierValue = 1

class AliceWebSocket():
	token = ''
	ws = None
	websocketUrl = ''
	segment=1
	instruments=list([])
	def __init__(self, token='', websocketUrl='', segment=1, instruments=[[1,1]]):
		self.token=token
		self.websocketUrl=websocketUrl
		self.segment=segment
		logger.info('Initializing websockets for alice with: %s%s'%(self.websocketUrl, self.token))
		logger.info('Instruments to be fetched:')
		logger.info(instruments)
		self.initialize(instruments)
	
	def initialize(self, instruments=[[1,1]]):
		websocket.enableTrace(False)
		self.instruments=instruments
		wssurl = '%s%s'%(self.websocketUrl,self.token)
		
		ws = websocket.WebSocketApp(wssurl,
									on_message=self.on_message,
									on_error=self.on_error,
									on_close=self.on_close)
		def on_open(ws):
			sub_packet = {"a": "subscribe", "v": instruments, "m": "marketdata" }
			def run(ws, sub_packet):
				ws.send(json.dumps(sub_packet))
				self.ws = ws
				while True:
					time.sleep(10)
					hb_packet = {"a": "h", "v": [], "m": ""}
					ws.send(json.dumps(hb_packet))
					ws.send(json.dumps(sub_packet))
			thread.start_new_thread(run, (ws,sub_packet,))
		ws.on_open = on_open
		ws.run_forever()
		self.ws = ws

	def on_message(ws, message):
		# logger.info('Message recieved:', message)
		marketdataPkt = CliMarketdataRes()
		if marketdataPkt.mode == 0 and len(message) != 86:
			logger.info('...heartbeat...')
			return
		global last_traded_price
		marketdataPkt.get_CliMarketdataRes_Instruct(message)
		last_traded_price = marketdataPkt.last_traded_price
		multiplierValue=multiplier[str(marketdataPkt.exchange_code)]
		datum = {
			'instrument_token':marketdataPkt.instrument_token, 
			'last_traded_price':(marketdataPkt.last_traded_price/multiplierValue), 
			'last_traded_time':marketdataPkt.last_traded_time, 
			'last_traded_quantity':marketdataPkt.last_traded_quantity, 
			'trade_volume':marketdataPkt.trade_volume, 
			'best_bid_price':(marketdataPkt.best_bid_price/multiplierValue), 
			'best_bid_quantity':marketdataPkt.best_bid_quantity, 
			'best_ask_price':(marketdataPkt.best_ask_price/multiplierValue), 
			'best_ask_quantity':marketdataPkt.best_ask_quantity, 
			'total_buy_quantity':marketdataPkt.total_buy_quantity, 
			'total_sell_quantity':marketdataPkt.total_sell_quantity, 
			'average_trade_price':(marketdataPkt.average_trade_price/multiplierValue), 
			'exchange_timestamp':marketdataPkt.exchange_timestamp, 
			'open_price':(marketdataPkt.open_price/multiplierValue), 
			'high_price':(marketdataPkt.high_price/multiplierValue), 
			'low_price':(marketdataPkt.low_price/multiplierValue), 
			'close_price':(marketdataPkt.close_price/multiplierValue), 
			'yearly_high_price':(marketdataPkt.yearly_high_price/multiplierValue), 
			'yearly_low_price':(marketdataPkt.yearly_low_price/multiplierValue)
		}
		logger.info(datum)
		producer.send(str(marketdataPkt.instrument_token), datum)
		producer.flush()
		# data_from_resource_server(access_token)
	
	def on_error(ws, error):
		logger.error('Error occurred:')
		logger.error(error)
		thread.exit()
	
	def on_close(ws):
		logger.info('...Feed data socket closed...')
		logger.info('Retrying again...')
		thread.exit()
