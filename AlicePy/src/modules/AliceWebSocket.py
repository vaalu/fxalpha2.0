#!/usr/bin/env python3
from modules.MarketData import CliMarketdataRes
import websocket
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

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
	def __init__(self, token='', websocketUrl='', segment=1, instruments=[[1,1]]):
		self.token=token
		self.websocketUrl=websocketUrl
		self.segment=segment
		print('Initializing websockets for alice with: %s%s'%(self.websocketUrl, self.token))
		print('Instruments to be fetched:', instruments)
		self.initialize(instruments)
	
	def initialize(self, instruments=[[1,1]]):
		websocket.enableTrace(False)
		wssurl = '%s%s'%(self.websocketUrl,self.token)
		
		ws = websocket.WebSocketApp(wssurl,
									on_message=self.on_message,
									on_error=self.on_error,
									on_close=self.on_close)
		def on_open(ws):
			sub_packet = {"a": "subscribe", "v": instruments, "m": "marketdata" }
			def run(*args):
				ws.send(json.dumps(sub_packet))
				self.ws = ws
			thread.start_new_thread(run, ())
		ws.on_open = on_open
		ws.run_forever()
		self.ws = ws

	def on_message(ws, message):
		# print('Message recieved:', message)
		marketdataPkt = CliMarketdataRes()
		if marketdataPkt.mode == 0 and len(message) != 86:
			print('heartbeat')
			ws.close()
			return
		global last_traded_price
		marketdataPkt.get_CliMarketdataRes_Instruct(message)
		last_traded_price = marketdataPkt.last_traded_price
		print('\n')
		print('exchange_code', marketdataPkt.exchange_code)
		multiplierValue=multiplier[str(marketdataPkt.exchange_code)]
		print('Segment multiplier to be fetched:', multiplierValue)
		
		print('instrument_token', marketdataPkt.instrument_token)
		print('last_traded_price', (marketdataPkt.last_traded_price/multiplierValue))
		print('last_traded_time', marketdataPkt.last_traded_time)
		print('last_traded_quantity', marketdataPkt.last_traded_quantity)
		print('trade_volume', marketdataPkt.trade_volume)
		print('best_bid_price', (marketdataPkt.best_bid_price/multiplierValue))
		print('best_bid_quantity', marketdataPkt.best_bid_quantity)
		print('best_ask_price', (marketdataPkt.best_ask_price/multiplierValue))
		print('best_ask_quantity', marketdataPkt.best_ask_quantity)
		print('total_buy_quantity', marketdataPkt.total_buy_quantity)
		print('total_sell_quantity', marketdataPkt.total_sell_quantity)
		print('average_trade_price', (marketdataPkt.average_trade_price/multiplierValue))
		print('exchange_timestamp', marketdataPkt.exchange_timestamp)
		print('open_price', (marketdataPkt.open_price/multiplierValue))
		print('high_price', (marketdataPkt.high_price/multiplierValue))
		print('low_price', (marketdataPkt.low_price/multiplierValue))
		print('close_price', (marketdataPkt.close_price/multiplierValue))
		print('yearly_high_price', (marketdataPkt.yearly_high_price/multiplierValue))
		print('yearly_low_price', (marketdataPkt.yearly_low_price/multiplierValue))
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
		producer.send(str(marketdataPkt.instrument_token), datum)
		producer.flush()
		# data_from_resource_server(access_token)
	
	def on_error(ws, error):
		print('Error occurred:', error)
	
	def on_close(ws):
		print('...Feed data socket closed...')
