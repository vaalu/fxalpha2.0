import datetime
import calendar
import time
from modules.AlphaStream import AlphaStrem
def main():
	print('Initializing 1 min processing...')
	AlphaStrem().process_ohlc()

if __name__ == "__main__":
	main()