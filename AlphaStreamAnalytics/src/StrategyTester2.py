from modules.analytics.MACDStrategy import MACDStrategy
from modules.util.RedisStrategyUtil import RedisStrategyUtil 
import time
def main():
	curr_min = 1592971200
	instr = 220239	
	macd = MACDStrategy.get_instance()
	red = RedisStrategyUtil()
	while curr_min <= 1592995380:
		curr, prev = red.fetch("MACD", instr, 1, curr_min, curr_min-60)
		if curr != None and curr != {}:
			curr["instrument_token"] = curr["instrument"]
			curr["last_traded_price"] = curr["close"]
			print(curr)
			macd.process(curr)
			time.sleep(2)
		curr_min += 60
if __name__ == "__main__":
	main()