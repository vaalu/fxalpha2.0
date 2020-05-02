import logging
from modules.tests.AliceTest1 import AliceInstruments
AliceInstruments().getCommodityInstruments()

# from modules.AlphaConsumer import AlphaConsumer
# AlphaConsumer().consume_messages()

# import modules.tests.KafkaTestConsumer
# import datetime
# import modules.tests.TestOperations
# jsts = 1588064271
# dt = datetime.datetime.fromtimestamp(jsts/1000)
# print(dt)

def main():
	logging.basicConfig(	format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', 
							filename='/var/log/alphapy.log', 
							level=logging.DEBUG)

if __name__ == "__main__":
	main()