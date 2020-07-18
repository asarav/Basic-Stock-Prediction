import data_retrieval.stockData as stockData
import matplotlib.pyplot as plt
import time
import datetime

stock = stockData.StockData('MSFT')

print(stock.quote)
print(stock.stockData)
start = str(datetime.date(2000, 1, 1))
end = str(datetime.date(2012, 1, 1))
print(stock.getHistoricalPrices(period='1d', start=start, end=end).head())

times = []
prices = []

for index, row in stock.historicalData.iterrows():
    #Convert date to int
    timestamp = float(index.to_julian_date())
    prices.append(row['Open'])
    times.append(timestamp)



#plt.plot(times, prices)
#plt.show()