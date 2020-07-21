#Calculates metrics based off of the closing price
class TimeSeriesMetricsCalculation:
    def __init__(self, data):
        self.data = data

    #Compute total avg, 5 day moving average, 15 day moving average, 100 day moving average, and 1 year moving average
    def movingAverages(self):
        #Get last 365 days
        last365 = self.data.tail(365)["Close"].mean()
        last100 = self.data.tail(100)["Close"].mean()
        last15 = self.data.tail(15)["Close"].mean()
        last5 = self.data.tail(5)["Close"].mean()
        return last5, last15, last100, last365

    #Compute autocorrelation with different lag values
    def autocorrelation(self, lag=1):
        return self.data["Close"].autocorr(lag)

    def movingAverageVolume(self):
        last365 = self.data.tail(365)["Volume"].mean()
        last100 = self.data.tail(100)["Volume"].mean()
        last15 = self.data.tail(15)["Volume"].mean()
        last5 = self.data.tail(5)["Volume"].mean()
        return last5, last15, last100, last365