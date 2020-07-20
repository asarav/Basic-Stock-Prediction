import data_retrieval.stockData as stockData
import datetime
from datetime import date
import utils.stockMetricCalculation as stockMetrics

#This will work as follows:
#1. For a certain stock, determine how the stock behaves one month later.
#2. The one month later is the label. Everything preceding the 1 month will be the data being classified
from utils.timeSeriesMetricsCalculation import TimeSeriesMetricsCalculation

stock = stockData.StockData('MSFT')

yearDifference = 15

startDate = datetime.date(2000, 1, 1)

for i in range(0, 100):
    print(i)
    start = str(startDate)
    startYear = startDate.year
    startMonth = startDate.month

    endMonth = startMonth
    endYear = startDate.year + yearDifference

    #If we run out of usable data, terminate
    if endYear == date.today().year and endMonth+1 >= date.today().month:
        break
    end = str(datetime.date(endYear, endMonth, 1))

    # Generate Data for Past
    print("Retrieve Past Data")
    pastData = stock.getHistoricalPrices('1d', start, end)
    metricCalculation = TimeSeriesMetricsCalculation(pastData)
    featureAverages = metricCalculation.movingAverages()
    autoCorrelations = metricCalculation.autocorrelation(), metricCalculation.autocorrelation(2), metricCalculation.autocorrelation(5), metricCalculation.autocorrelation(10)
    featureVolumeAverages = metricCalculation.movingAverageVolume()

    # Generate Data for one month in the future
    monthLaterMonth = endMonth + 1
    monthLaterYear = endYear
    if monthLaterMonth > 12:
        monthLaterMonth = 1
        monthLaterYear = endYear + 1

    print("Retrieve One Month Later")
    oneMonthLater = str(datetime.date(monthLaterYear, monthLaterMonth, 1))
    oneMonthLaterData = stock.getHistoricalPrices('1d', end, oneMonthLater)

    metrics = stockMetrics.StockMetricCalculation(oneMonthLaterData)
    avgPrice = metrics.avgPrice()
    highestIncrease = metrics.highestIncrease()
    highestDecrease = metrics.highestDecrease()
    change = metrics.change()
    score = metrics.score()
    labels = [avgPrice, highestIncrease, highestDecrease, change, score]

    #Increment month for start
    if startDate.month == 12:
        startDate = datetime.date(startDate.year + 1, 1, 1)
    else:
        startDate = datetime.date(startDate.year, startDate.month + 1, 1)

