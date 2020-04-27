#!/usr/bin/env python3
import json
from flask import Flask, request
from modules.Alice import Alice
from modules.EquitiesData import EquitiesData
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
	'NIFTY50_URL' : config.get('TRADING_INSTRUMENTS', 'nifty50.url'), 
	'COMMODITIES': json.loads(config.get('TRADING_INSTRUMENTS', 'instruments.commodities'))
}
alice = Alice()
class Commodities():
	def __init__(self):
		print('Fetching data for commodities')
		wssUrl = '%s?access_token='%(aliceAnt['URL_WSS'])
		instr = self.fetchForInstruments()
	def fetchForInstruments(self):
		return alice.fetchCommoditiesLive()
class Equities():
	def __init__(self, segment=1):
		print('Fetching data for segment: %i'%(segment))
		instr = self.fetchForInstruments()
	def fetchForInstruments(self):
		return alice.fetchNifty50Live()

app = Flask(__name__)

@app.route("/",methods=['GET'])
def invoke():
	def runF(*args):
		inite = Commodities()
		print('Initialized for commodities data')
	thread.start_new_thread(runF, ())
	def runE(*args):
		initf = Equities(segment=4)
		print('Initialized for equities data')
	thread.start_new_thread(runE, ())
	return 'WebSocket established with token:%s'%(alice.access_token)
	# return 'WebSocket established without token'

@app.route("/instruments",methods=['GET'])
def instruments():
	return {"instruments" : alice.fetchNifty50()}
	# return {"instruments" : [[1,15083], [1,236], [1,5900], [1,16669], [1,317], [1,16675], [1,526], [1,10604], [1,29135], [1,547], [1,694], [1,20374], [1,881], [1,910], [1,4717], [1,1232], [1,7229], [1,1333], [1,1348], [1,1363], [1,1394], [1,1330], [1,4963], [1,1660], [1,1624], [1,5258], [1,1594], [1,11723], [1,1922], [1,11483], [1,2031], [1,10999], [1,11630], [1,17963], [1,2475], [1,14977], [1,2885], [1,3103], [1,3045], [1,3351], [1,11536], [1,3456], [1,3499], [1,13538], [1,3506], [1,11287], [1,11532], [1,3063], [1,3787], [1,3812]]}

@app.route("/shutdown",methods=['GET'])
def stopServer():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return 'Alice Websocket client stopped'

if __name__ == "__main__":
	app.run()