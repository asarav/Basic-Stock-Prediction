import yfinance as yf
import pandas as pd
import datetime

class StockData:
    def __init__(self, tickerSymbol='AAPL'):
        #define the ticker symbol
        self.quote = tickerSymbol
        #get data on this ticker. This creates a ticker object
        self.stockData = yf.Ticker(self.quote)

    def getHistoricalPrices(self, period='1d', start='2010-1-1', end='2020-1-25'):
        #get the historical prices for this ticker
        self.historicalData = self.stockData.history(period=period, start=start, end=end)
        return self.historicalData

    def getAllHistory(self):
        self.AllHistoricalData = self.stockData.history(period="max")
        return self.AllHistoricalData

    #Called after get all history to reduce network calls.
    def getHistoricalPricesSubset(self, period, start, end):
        self.historicalData = self.AllHistoricalData.loc[start:end]
        date = str(self.historicalData.index[-1]).split(" ")
        if date[0] == end:
            val = self.historicalData.tail(1).index
            self.historicalData = self.historicalData.drop(val)
        return self.historicalData

    def getStart(self):
        return str(self.AllHistoricalData.index[0]).split(" ")[0]

    # Duration will be based off of distance to current year. Needs improvement
    def suggestedStartAndDuration(self):
        start = self.getStart().split("-")
        year = int(start[0])+1
        duration = 10
        if year < 2000:
            year = 2000
            duration = 12
        elif year < 2005:
            duration = 10
        elif year < 2010:
            duration = 7
        elif year < 2012:
            duration = 6
        elif year < 2015:
            duration = 4
        elif year < 2017:
            duration = 2
        else:
            duration = 1
        startDate = datetime.date(year, 1, 1)
        return startDate, duration

    # https://github.com/ranaroussi/yfinance/pull/371
    def info(self):
        return self.stockData.info

    def events(self):
        return self.stockData.calendar

    def analystRecommendations(self):
        return self.stockData.recommendations