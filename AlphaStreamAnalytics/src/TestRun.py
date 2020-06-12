from modules.util.DateTimeUtil import DateTimeUtil
from modules.AlphaStream import AlphaStrem
# from modules.EODProcessing import EODProcessor
# from modules.CalculationsProcessor import CalculationsProcessor

def main():
	date_util = DateTimeUtil()
	print('Initializing processing...%s'%date_util.get_current_local_time())
	# EODProcessor().initialize_1_min_process()
	AlphaStrem().process_ohlc()
	# CalculationsProcessor(date_util).process_calculations()
if __name__ == "__main__":
	main()