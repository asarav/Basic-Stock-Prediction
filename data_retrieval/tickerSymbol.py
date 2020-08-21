import urllib.request
import pandas as pd

class TickerSymbols:
	def __init__(self):
		url = "https://www.sec.gov/include/ticker.txt"
		file = urllib.request.urlopen(url)
		self.symbols = []
		for line in file:
			decoded_line = line.decode("utf-8")
			# Tickers with dashes are not useful
			if "-" not in decoded_line.split()[0]:
				self.symbols.append(decoded_line.split()[0])

		table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
		self.sAndP = table[0]["Symbol"].tolist()