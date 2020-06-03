from modules.props.ConfigProps import AppLogger
from modules.util.SingleInstanceUtil import SingleInstanceUtil
from modules.Alice import Alice
from flask import Flask, request
try:
	import thread
except ImportError:
	import _thread as thread
import time

app = Flask(__name__)

logger = AppLogger('AlphaWeb')
alice = Alice()

@app.route("/",methods=['GET'])
def invoke():
	alice.initiaize_instruments()
	def runF(*args):
		alice.fetchCommoditiesLive()
		logger.info('Initialized for commodities data')
	thread.start_new_thread(runF, ())
	def runE(*args):
		alice.fetchNifty50Live()
		logger.info('Initialized for equities data')
	thread.start_new_thread(runE, ())

	return 'Alpha connected with token:%s'%(alice.access_token)

@app.route("/shutdown",methods=['GET'])
def stopServer():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return 'Alpha Web stopped'

if __name__ == "__main__":
	app.run()




