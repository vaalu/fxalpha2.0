import logging
from modules.util.AliceInstrumentsUtil import AliceInstruments

def main():
	AliceInstruments().fetch_commodities()
if __name__ == "__main__":
	main()