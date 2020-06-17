from modules.props.ConfigProps import AppCalcLogger
from pandas import pandas as pd
import ta

class RSI():
	__period = 14
	def get_period(self):
		return self.__period
	def calculate(self, data):
		df = pd.DataFrame(data)
		indicator = ta.momentum.rsi(close=df["close"], n=self.__period, fillna=True)
		df["rsi"] = indicator
		return ["rsi"], df.to_dict(orient='records')
		
