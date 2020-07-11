import data_retrieval.stockData as stockData
import matplotlib.pyplot as plt
import time
import datetime

stock = stockData.StockData('MSFT')

print(stock.quote)
print(stock.stockData)
print(stock.getHistoricalPrices().head())

times = []
prices = []

for index, row in stock.historicalData.iterrows():
    #Convert date to int
    timestamp = float(index.to_julian_date())
    prices.append(row['Open'])
    times.append(timestamp)

plt.plot(times, prices)
plt.show()