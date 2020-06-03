import datetime
import calendar
import time
from modules.AlphaStream import AlphaStrem
from modules.EODProcessing import EODProcessor
def main():
	print('Initializing 1 min processing...')
	EODProcessor().initialize_1_min_process()
	# AlphaStrem().process_ohlc()

if __name__ == "__main__":
	main()