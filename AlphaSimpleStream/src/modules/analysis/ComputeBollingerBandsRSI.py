import ta
import numpy
import datetime
import calendar
import time

class ComputeBollingerBand():
	def __init__(self):
		today_date = datetime.datetime.now()
		start_time = datetime.datetime(today_date.year, today_date.month, today_date.day, 9, 0, 0)
		print(start_time)

