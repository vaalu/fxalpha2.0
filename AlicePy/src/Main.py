#!/usr/bin/env python3
import json
from flask import Flask, request
from modules.AliceWebSocket import AliceWebSocket
import configparser
from cryptography.fernet import Fernet

try:
	import thread
except ImportError:
	import _thread as thread
import time


print('Fetching access token from alice blue ant API')
config = configparser.ConfigParser()
config.read('application.config.properties')

aliceAnt = {
	'CLIENT_ID' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.id'), 
	'CLIENT_USER' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.user'), 
	'CLIENT_SECRET' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.secret'), 
	'CLIENT_PASSWORD' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.password'), 
	'URL_AUTH' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.auth'), 
	'URL_TOKEN' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.token'), 
	'URL_CALLBACK' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.callback'), 
	'URL_LOGIN' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.login'),
	'URL_2FA' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.2fa'),
	'URL_WSS' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.wss'), 
	'ALICE_API_BASE': config.get('ALICE_ANT_API', 'alice.ant.api.base'),
	'ALICE_PROFILE' : config.get('ALICE_ANT_API', 'alice.ant.api.profile'),
	'NIFTY_50_STOCKS':json.loads(config.get('TRADING_INSTRUMENTS', 'instruments.nifty.50')),
	'COMMODITIES':json.loads(config.get('TRADING_INSTRUMENTS', 'instruments.commodities'))
}

class Main():
	segment=1

	def __init__(self, segment=1, token=''):
		print('Fetching data for segment: %i with token %s'%(segment, token))
		wssUrl = '%s?access_token='%(aliceAnt['URL_WSS'])
		instr = self.fetchForInstruments()
		ws = AliceWebSocket(websocketUrl=wssUrl, 
							token=token,
							instruments=instr)
	def fetchForInstruments(self):
		return aliceAnt['COMMODITIES']
class Equities():
	segment=1

	def __init__(self, segment=1, token=''):
		print('Fetching data for segment: %i with token %s'%(segment, token))
		wssUrl = '%s?access_token='%(aliceAnt['URL_WSS'])
		instr = self.fetchForInstruments()
		ws = AliceWebSocket(websocketUrl=wssUrl, 
							token=token,
							instruments=instr)
	def fetchForInstruments(self):
		return aliceAnt['NIFTY_50_STOCKS']

app = Flask(__name__)

@app.route("/<token>",methods=['GET'])
def invoke(token):
	def runF(*args):
		inite = Main(segment=4, token=token)
		print('Initialized for commodities data')
	thread.start_new_thread(runF, ())
	def runE(*args):
	 	initf = Equities(segment=4, token=token)
	 	print('Initialized for equities data')
	thread.start_new_thread(runE, ())
	return 'WebSocket established with token:%s'%(token)

@app.route("/shutdown",methods=['GET'])
def stopServer():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return 'Alice Websocket client stopped'

if __name__ == "__main__":
	app.run()