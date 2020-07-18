import yfinance as yf

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

    def info(self):
        return self.stockData.info

    def events(self):
        return self.stockData.calendar

    def analystRecommendations(self):
        return self.stockData.recommendations