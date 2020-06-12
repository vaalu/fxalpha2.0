import ta
import json
from pandas import pandas as pd

class BollingerBands():
	__period = 20
	__standard_deviation = 2
	def get_period(self):
		return self.__period
	def get_standard_deviation(self):
		return self.__standard_deviation
	def calculate(self, data):
		df = pd.DataFrame(data)
		indicator = ta.volatility.BollingerBands(close=df["close"], n=self.__period, ndev=self.__standard_deviation)
		df["bb_bbm"] = indicator.bollinger_mavg()
		df["bb_bbh"] = indicator.bollinger_hband()
		df["bb_bbl"] = indicator.bollinger_lband()
		return ["bb_bbh", "bb_bbm", "bb_bbl"], df.to_dict(orient='records')
		