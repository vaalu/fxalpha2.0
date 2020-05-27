import datetime
import calendar
import time
from modules.AlphaConsumerLegacy import AlphaConsumerLegacy
from modules.Nifty50Instruments import Nifty50

def time_tests():
	print('Calculating bollinger bands')
	today_date = datetime.datetime.now()
	start_time = datetime.datetime(today_date.year, today_date.month, today_date.day, 9, 0, 0)
	print(start_time)

	# jsts = 1588615200
	jsts = 1588701599
	dt = datetime.datetime.fromtimestamp(jsts).isoformat()
	print(dt)
	isodate = calendar.timegm(time.gmtime())
	print(isodate)
	print(isodate - 60)
	
	date_time_str = '2020-05-04 09:00:00'
	date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
	print('Date:', date_time_obj.date())
	
	time_tuple = date_time_obj.timetuple()
	print('Date Time:', time.mktime(time_tuple))
	
	nine_rep = time.mktime(time_tuple)
	nine_rep_5 = int(nine_rep + (60 * 5))
	print(nine_rep_5)
	print(datetime.datetime.fromtimestamp(nine_rep_5).isoformat())

	current_date = datetime.datetime.today()
	print(current_date)


def main():
	AlphaConsumerLegacy().consume_messages()
if __name__ == "__main__":
	main()