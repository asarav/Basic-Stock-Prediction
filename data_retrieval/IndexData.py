#File to retrieve data from S&P, DOW, and NASDAQ based on period data
from data_retrieval.stockData import StockData

class IndexData:
    def __init__(self, period='1d', start='2010-1-1', end='2020-1-25'):
        self.SANDP = StockData('INX')
        self.DOW = StockData('^DJI')
        self.NASDAQ = StockData('NDAQ')

        self.SANDPData = self.SANDP.stockData.history(period=period, start=start, end=end)
        self.DOWData = self.DOW.stockData.history(period=period, start=start, end=end)
        self.NASDAQData = self.NASDAQ.stockData.history(period=period, start=start, end=end)

    def autocorrelation(self, lag=1):
        return self.SANDPData["Close"].autocorr(lag), self.DOWData["Close"].autocorr(lag), self.NASDAQData["Close"].autocorr(lag)

    def movingAverages(self, data):
        #Get last 365 days
        last365 = data.tail(365)["Close"].mean()
        last100 = data.tail(100)["Close"].mean()
        last15 = data.tail(15)["Close"].mean()
        last5 = data.tail(5)["Close"].mean()
        return last5, last15, last100, last365

    def movingAverageVolume(self, data):
        last365 = data.tail(365)["Volume"].mean()
        last100 = data.tail(100)["Volume"].mean()
        last15 = data.tail(15)["Volume"].mean()
        last5 = data.tail(5)["Volume"].mean()
        return last5, last15, last100, last365
