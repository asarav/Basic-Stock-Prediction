import training.model as model
import data_retrieval.tickerSymbol as tickerSymbol
import data_retrieval.MonthLaterData as oneMonthData
from sklearn.linear_model import LinearRegression
import data_retrieval.stockData as stockData
import math
from colorama import Fore, Back, Style
from datetime import datetime
import pandas as pd

class Train:
    output = {}
    def __init__(self, quote=None, printGraph=False, callback=None, outputExcel=False, useSAndP=False, useRussell1000=False, monthsLater=1, streamlit=False):
        self.printGraph = printGraph
        self.callback = callback
        self.outpuExcel = outputExcel
        self.monthsLater = monthsLater
        self.streamlit = streamlit
        excel = pd.DataFrame(columns=['Symbol',
                                        'Current Price',
                                        'Future Price',
                                        'Percent Increase',
                                        'Error',
                                        'Error Percentage',
                                        'Floor',
                                        'Ceiling',
                                        'Variance Score'])
        if quote is None:
            ticker = tickerSymbol.TickerSymbols()
            symbols = ticker.symbols
            if useSAndP:
                symbols = ticker.sAndP
            elif useRussell1000:
                symbols = ticker.russell1000
            print(str(len(symbols)) + " total symbols")
            count = 0
            for symbol in symbols:
                print(Fore.YELLOW + "PROGRESS: ", count, len(symbols), (count/len(symbols)))
                print(Fore.BLUE + "Processing: ", symbol)
                print(Style.RESET_ALL)
                data = self.runTraining(symbol)
                if data is not None and outputExcel:
                    excel = pd.concat([excel, data])
                count = count + 1
            if outputExcel:
                excel.to_csv("Predictions " + str(monthsLater) + ".csv")

        else:
            self.runTraining(quote)

    def runTraining(self, symbol):
        try:
            #start = datetime.now()
            #print(start.hour, ':', start.minute, ':', start.second, '.', start.microsecond)

            print("Retrieving Stock Data")
            data = oneMonthData.MonthLaterData(symbol, monthsLater=self.monthsLater)

            features = data.features
            labels = data.labels

            print("Training Model on Data")

            trainedModel = model.Model(features, labels, data.currentData, symbol, LinearRegression)

            print("Model Trained")

            results = trainedModel.trainWithCrossVal()
            self.output["CrossVal Results"] = results
            stock = stockData.StockData(symbol)
            info = stock.info()
            self.output["CurrentPrice"] = info["previous_close"]
            self.output["Future Price"] = trainedModel.predictCurrentMonth()[0]
            self.output["Percent Increase"] = 0
            if info["previous_close"] > 0:
                self.output["Percent Increase"] = (trainedModel.predictCurrentMonth()[0]/info["previous_close"] - 1)*100
            print("Current Price: ", self.output["CurrentPrice"])
            print("Predicted Price: ", self.output["Future Price"])
            print("Predicted Percent Change in Price: ", self.output["Percent Increase"], "%")

            mse = results["test_mean_squared_error"]
            rootMSE = math.sqrt(mse)
            varianceScore = results["variance_score"]

            print("Error Margin: ", rootMSE)
            errorPercentage = 0
            if self.output["CurrentPrice"] > 0:
                errorPercentage = (rootMSE / self.output["CurrentPrice"]) * 100
                print("Error Percentage: ", errorPercentage)
            floor = self.output["Future Price"] - rootMSE
            ceiling = self.output["Future Price"] + rootMSE
            print("Predicted Floor: ", floor)
            print("Predicted Ceiling: ", ceiling)
            
            print("Variance Score: ", varianceScore)

            if floor > self.output["CurrentPrice"]:
                print(Fore.GREEN + "Predicted Gains GUARANTEED")
                print(Style.RESET_ALL)
                self.output["Message"] = "Predicted GAINS Highly Likely given Error values"
            if ceiling < self.output["CurrentPrice"]:
                print(Fore.RED + "Predicted Losses GUARANTEED")
                print(Style.RESET_ALL)
                self.output["Message"] = "Predicted LOSSES Highly Likely given Error values"

            #end = datetime.now()
            #print(end.hour, ':', end.minute, ':', end.second, '.', end.microsecond)

            if self.printGraph:
                trainedModel.comparePredictions(streamlit=self.streamlit)
                if self.callback is not None:
                    self.callback()
            return pd.DataFrame(data=[[symbol, self.output["CurrentPrice"], self.output["Future Price"], self.output["Percent Increase"], rootMSE, errorPercentage, floor, ceiling, varianceScore]],
                               columns=['Symbol',
                                        'Current Price',
                                        'Future Price',
                                        'Percent Increase',
                                        'Error',
                                        'Error Percentage',
                                        'Floor',
                                        'Ceiling',
                                        'Variance Score'])
        except Exception as e:
            print(e)
            if "Data doesn't exist for startDate" in str(e):
                print("This is a newer company")
            else:
                print(e)