import data_retrieval.stockData as stockData
import datetime
from datetime import date
import utils.stockMetricCalculation as stockMetrics
from data_retrieval.IndexData import IndexData
from utils.timeSeriesMetricsCalculation import TimeSeriesMetricsCalculation
import pandas as pd

#This will work as follows:
#1. For a certain stock, determine how the stock behaves one month later.
#2. The one month later is the label. Everything preceding the 1 month will be the data being classified
class MonthLaterData:
    #Keep months later below 1 year
    def __init__(self, quote='MSFT', monthsLater=1):
        stock = stockData.StockData(quote)
        stock.getAllHistory()
        startDate, yearDifference = stock.suggestedStartAndDuration()

        featureFrame = pd.DataFrame(columns=['avg365',
                                             'avg100',
                                             'avg15',
                                             'avg5',
                                             'autocorrelation1',
                                             'autocorrelation2',
                                             'autocorrelation5',
                                             'autocorrelation10',
                                             'volAvg365',
                                             'volAvg100',
                                             'volAvg15',
                                             'volAvg5',
                                             'initialPrice'])
        labelFrame = pd.DataFrame(columns=['finalPrice',
                                             'score',
                                             'change'])

        for i in range(0, 1200):
            start = str(startDate)

            endMonth = startDate.month
            endYear = startDate.year + yearDifference

            end = str(datetime.date(endYear, endMonth, 1))

            # Generate Data for Past
            #pastData = stock.getHistoricalPrices('1d', start, end)
            pastData = stock.getHistoricalPricesSubset('1d', start, end)
            metricCalculation = TimeSeriesMetricsCalculation(pastData)
            featureAverages = metricCalculation.movingAverages()
            autoCorrelations = metricCalculation.autocorrelation(), metricCalculation.autocorrelation(2), metricCalculation.autocorrelation(5), metricCalculation.autocorrelation(10)
            featureVolumeAverages = metricCalculation.movingAverageVolume()

            startingPrice = pastData.tail(1)["Close"][0]

            #Add row to dataframes
            df2 = pd.DataFrame(data=[[featureAverages[3],
                                     featureAverages[2],
                                     featureAverages[1],
                                     featureAverages[0],
                                     autoCorrelations[0],
                                     autoCorrelations[1],
                                     autoCorrelations[2],
                                     autoCorrelations[3],
                                     featureVolumeAverages[3],
                                     featureVolumeAverages[2],
                                     featureVolumeAverages[1],
                                     featureVolumeAverages[0],
                                     startingPrice]],
                               columns=['avg365',
                                             'avg100',
                                             'avg15',
                                             'avg5',
                                             'autocorrelation1',
                                             'autocorrelation2',
                                             'autocorrelation5',
                                             'autocorrelation10',
                                             'volAvg365',
                                             'volAvg100',
                                             'volAvg15',
                                             'volAvg5',
                                             'initialPrice'])

            #If we run out of usable data, terminate
            if endYear == date.today().year and endMonth >= date.today().month:
                print("Current Data is " + str(end))
                self.currentDate = str(end)
                self.currentData = df2.dropna()
                break

            #indexPastData = IndexData('1d', start, end)

            # Generate Data for x months in the future
            monthLaterMonth = endMonth + monthsLater
            monthLaterYear = endYear
            if monthLaterMonth > 12:
                monthLaterMonth = monthLaterMonth - 12
                monthLaterYear = endYear + 1

            monthLater = str(datetime.date(monthLaterYear, monthLaterMonth, 1))

            if not(monthLaterYear > date.today().year or (monthLaterYear == date.today().year and monthLaterMonth > date.today().month )):
                oneMonthLaterData = stock.getHistoricalPricesSubset('1d', end, monthLater)

                metrics = stockMetrics.StockMetricCalculation(oneMonthLaterData)
                avgPrice = metrics.avgPrice()
                highestIncrease = metrics.highestIncrease()
                highestDecrease = metrics.highestDecrease()
                change = metrics.change()
                score = metrics.score()
                finalPrice = metrics.getLastRow()
                labels = [avgPrice, highestIncrease, highestDecrease, change, score, finalPrice]

                df3 = pd.DataFrame(data=[[finalPrice,
                                          score,
                                          change
                                          ]],
                                   columns=['finalPrice',
                                            'score',
                                            'change'])

                featureFrame = pd.concat([featureFrame, df2])
                labelFrame = pd.concat([labelFrame, df3])

            #Increment month for start
            if startDate.month == 12:
                startDate = datetime.date(startDate.year + 1, 1, 1)
            else:
                startDate = datetime.date(startDate.year, startDate.month + 1, 1)

        #featureFrame.to_csv(quote + 'features.csv')
        #labelFrame.to_csv(quote + 'labels.csv')

        self.features = featureFrame.dropna()
        self.labels = labelFrame.dropna()
