import datetime
import calendar
import time
# from modules.SolrConfig import SolrConfig
from modules.RedisUtil2 import RedisUtil2
from modules.Nifty50Instruments import Nifty50
from modules.props.ConfigProps import InstrumentMapper
from modules.analysis.ComputeBollingerBandsRSI import ComputeBollingerBand

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
	# prepare = SolrConfig()
	# prepare.create_cores_for_instruments()
	n50 = Nifty50()
	equities = n50.fetchNifty50()
	for equity in equities:
		if equity != 'M&M':
			instr_id = InstrumentMapper[equity]
			print('Collecting for instrument: %s'%(instr_id))
			redutil = RedisUtil2(instr_id).readForInstrument()
	# instr_id = InstrumentMapper['ADANIPORTS']
	# redutil = RedisUtil2(instr_id).readForInstrument()
	ComputeBollingerBand()
if __name__ == "__main__":
	main()