from modules.util.DateTimeUtil import DateTimeUtil
from modules.AlphaStream import AlphaStream
def main():
	__date_util = DateTimeUtil.get_instance()
	st, eq_end, cm_end = __date_util.get_market_timings()
	curr = __date_util.get_local_time()
	print('Current market timings: start: %f: end equities: %f : end commodities: %f : curr local: %f'%(st, eq_end, cm_end, curr))
	AlphaStream().process_ohlc()
if __name__ == "__main__":
	main()