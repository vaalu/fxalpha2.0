import ta
import json
from pandas import pandas as pd

class KeltnerChannel():
	__n_period = 20
	__n_atr = 10
	def get_config(self):
		return self.__n_period, self.__n_atr
	def calculate(self, data):
		df = pd.DataFrame(data)
		indicator = ta.volatility.KeltnerChannel(high=df["high"], low=df["low"], close=df["close"])
		df["kc_hband"] = indicator.keltner_channel_hband()
		df["kc_mband"] = indicator.keltner_channel_mband()
		df["kc_lband"] = indicator.keltner_channel_lband()
		return ["kc_hband", "kc_mband", "kc_lband"], df.to_dict(orient='records')

