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
class OneMonthData:
    def __init__(self, quote='MSFT'):
        stock = stockData.StockData(quote)
        yearDifference = 15
        startDate = datetime.date(2000, 1, 1)
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

            #indexPastData = IndexData('1d', start, end)

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
            startingPrice = metrics.getFirstRow()
            finalPrice = metrics.getLastRow()
            labels = [avgPrice, highestIncrease, highestDecrease, change, score, finalPrice]

            #Increment month for start
            if startDate.month == 12:
                startDate = datetime.date(startDate.year + 1, 1, 1)
            else:
                startDate = datetime.date(startDate.year, startDate.month + 1, 1)

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

            featureFrame = pd.concat([featureFrame, df2])

            df3 = pd.DataFrame(data=[[finalPrice,
                                    score,
                                    change
                                ]],
                               columns=['finalPrice',
                                        'score',
                                        'change'])

            labelFrame = pd.concat([labelFrame, df3])

        #featureFrame.to_csv(quote + 'features.csv')
        #labelFrame.to_csv(quote + 'labels.csv')
        self.features = featureFrame
        self.labels = labelFrame
