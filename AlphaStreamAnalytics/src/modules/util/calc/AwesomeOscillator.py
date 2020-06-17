import ta
import json
from pandas import pandas as pd

class AwesomeOscillator():
	__short_period = 5
	__long_period = 34
	def get_config(self):
		return self.__short_period, self.__long_period
	def calculate(self, data):
		df = pd.DataFrame(data)
		indicator = ta.momentum.AwesomeOscillatorIndicator(df["high"], df["low"], s=self.__short_period, len=self.__long_period, fillna=True)
		df["ao"] = indicator.ao()
		return ["ao"], df.to_dict(orient='records')