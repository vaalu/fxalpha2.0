import logging
from flask import Flask, request
from modules.Alice import Alice
from modules.props.ConfigProps import aliceAnt, AppLogger
try:
	import thread
except ImportError:
	import _thread as thread
import time

logger = AppLogger()
alice = Alice()
alice.updateTopicsToKafka()

app = Flask(__name__)
class Commodities():
	def __init__(self):
		logger.info('Fetching data for commodities')
		wssUrl = '%s?access_token='%(aliceAnt['URL_WSS'])
		instr = self.fetchForInstruments()
	def fetchForInstruments(self):
		return alice.fetchCommoditiesLive()
class Equities():
	def __init__(self, segment=1):
		logger.info('Fetching data for segment: %i'%(segment))
		instr = self.fetchForInstruments()
	def fetchForInstruments(self):
		return alice.fetchNifty50Live()

@app.route("/",methods=['GET'])
def invoke():
	def runF(*args):
		inite = Commodities()
		logger.info('Initialized for commodities data')
	thread.start_new_thread(runF, ())
	def runE(*args):
		initf = Equities(segment=4)
		logger.info('Initialized for equities data')
	thread.start_new_thread(runE, ())
	return 'WebSocket established with token:%s'%(alice.access_token)

@app.route("/instruments",methods=['GET'])
def instruments():
	return {"instruments" : alice.fetchNifty50()}

@app.route("/shutdown",methods=['GET'])
def stopServer():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return 'Alice Websocket client stopped'

if __name__ == "__main__":
	app.run()




