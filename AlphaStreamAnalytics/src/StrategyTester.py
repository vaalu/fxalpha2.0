from modules.analytics.StrategiesPlug import StrategiesPlug
import time
def main():
	curr_min = 1592971200
	instr = 220239	
	macd = StrategiesPlug.get_instance()
	while curr_min <= 1592995380:
		macd.analyze(instr, 1, curr_min)
		print('%i:%i'%(instr, curr_min))
		# time.sleep(10)
		curr_min += 60
if __name__ == "__main__":
	main()