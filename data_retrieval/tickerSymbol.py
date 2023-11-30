import urllib.request
import pandas as pd

class TickerSymbols:
	def __init__(self):
		url = "https://www.sec.gov/include/ticker.txt"
		heads = {'Host': 'www.sec.gov', 'Connection': 'close',
				 'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
				 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
				 }
		request = urllib.request.Request(url=url, headers=heads)
		file = urllib.request.urlopen(request)
		self.symbols = []
		for line in file:
			decoded_line = line.decode("utf-8")
			# Tickers with dashes are not useful
			if "-" not in decoded_line.split()[0]:
				self.symbols.append(decoded_line.split()[0])

		table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
		#0 is the index of the symbol
		self.sAndP = table[0]["Symbol"].tolist()

		self.russell1000 = pd.read_csv("../resources/Russell1000.csv")["Symbol"].tolist()