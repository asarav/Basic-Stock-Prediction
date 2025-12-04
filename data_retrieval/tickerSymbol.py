import requests
import pandas as pd
import urllib.request

class TickerSymbols:
    def __init__(self):
        url = "https://www.sec.gov/include/ticker.txt"
        heads = {
            'Host': 'www.sec.gov',
            'Connection': 'close',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }
        request = urllib.request.Request(url=url, headers=heads)
        file = urllib.request.urlopen(request)

        self.symbols = []
        for line in file:
            decoded_line = line.decode("utf-8")
            if "-" not in decoded_line.split()[0]:  # skip tickers with dashes
                self.symbols.append(decoded_line.split()[0])

        wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        wiki_headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(wiki_url, headers=wiki_headers)
        response.raise_for_status()

        table = pd.read_html(response.text)
        self.sAndP = table[1]["Symbol"].tolist()

        self.russell1000 = pd.read_csv("../resources/Russell1000.csv")["Symbol"].tolist()
