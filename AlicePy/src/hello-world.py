import websocket
import json

try:
	import thread
except ImportError:
	import _thread as thread
import time
token='nRlhUZdN_qJYIVdeRudpNzIX0qNUJPbN1JaDo6tY1dc.CLiBL8NofykbPu40YPJX18xvdxeNznhSA5dM-OkfLv0'

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    sub_packet = {"a": "subscribe", "v": [[4, 217158]], "m": "marketdata" }
    def run(*args):
        ws.send(json.dumps(sub_packet))
    thread.start_new_thread(run, ())

websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://ant.aliceblueonline.com/hydrasocket/v2/websocket?access_token={token}",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
ws.on_open = on_open
ws.run_forever()
