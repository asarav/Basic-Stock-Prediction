import urllib.request

class TickerSymbols:
	def __init__(self):
		url = "https://www.sec.gov/include/ticker.txt"
		file = urllib.request.urlopen(url)
		self.symbols = []
		for line in file:
			decoded_line = line.decode("utf-8")
			self.symbols.append(decoded_line.split()[0])
