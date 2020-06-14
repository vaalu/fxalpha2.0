# from modules.CalculationsProcessor import CalculationsProcessor
from modules.AlphaStream import AlphaStrem
def main():
	AlphaStrem().process_ohlc()
	# CalculationsProcessor.get_instance().process_1_min_calc(1591721520)
if __name__ == "__main__":
	main()