#Calculates metrics based off of the closing price
class StockMetricCalculation:
    def __init__(self, data):
        self.data = data

    #Highest increase from the starting closing price
    def highestIncrease(self):
        first = self.getFirstRow()
        diff = 0
        highestValue = first
        for index, row in self.data.iterrows():
            if (row['Close'] - first) > diff:
                diff = row['Close'] - first
                highestValue = row['Close']
        return diff

    #Highest decrease from the starting price
    def highestDecrease(self):
        first = self.getFirstRow()
        diff = 0
        lowestValue = first
        for index, row in self.data.iterrows():
            if (first - row['Close']) > diff:
                diff = first - row['Close']
                lowestValue = row['Close']
        return diff

    def change(self):
        return self.getLastRow() - self.getFirstRow()

    #Average price over the period
    def avgPrice(self):
        return self.data["Close"].mean()

    def getFirstRow(self):
        return self.data.head(1)["Close"][0]

    def getLastRow(self):
        return self.data.tail(1)["Close"][0]

    def score(self):
        change = self.change()
        highestIncrease = self.highestIncrease()
        highestDecrease = self.highestDecrease()
        normalizedAvg = self.avgPrice()/self.getFirstRow()
        return normalizedAvg * (change +  highestIncrease + (highestDecrease * 0.5))

