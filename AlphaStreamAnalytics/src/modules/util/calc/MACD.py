import ta
import json
from pandas import pandas as pd

class MACD():
	__n_fast = 12
	__n_slow = 26
	__n_sign = 9
	def get_config(self):
		return self.__n_slow, self.__n_fast, self.__n_sign
	def calculate(self, data):
		df = pd.DataFrame(data)
		indicator = ta.trend.MACD(close=df["close"], n_slow=self.__n_slow, n_fast=self.__n_fast, n_sign=self.__n_sign, fillna=True)
		macd = indicator.macd()
		hist = indicator.macd_diff()
		df["macd"] = macd
		df["histogram"] = hist
		return ["macd"], df.to_dict(orient='records')

