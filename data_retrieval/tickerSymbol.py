import urllib.request

url = "https://www.sec.gov/include/ticker.txt"
file = urllib.request.urlopen(url)

for line in file:
	decoded_line = line.decode("utf-8")
	print(decoded_line)