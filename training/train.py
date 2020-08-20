import training.model as model
import data_retrieval.tickerSymbol as tickerSymbol
import data_retrieval.OneMonthData as oneMonthData
from sklearn.linear_model import LinearRegression
import data_retrieval.stockData as stockData
import math
from colorama import Fore, Back, Style
from datetime import datetime

class Train:
    output = {}
    def __init__(self, quote=None, printGraph=False, callback=None):
        self.printGraph = printGraph
        self.callback = callback
        if quote is None:
            ticker = tickerSymbol.TickerSymbols()
            print(str(len(ticker.symbols)) + " total symbols")
            for symbol in ticker.symbols:
                print(Fore.BLUE + "Processing: ", symbol)
                print(Style.RESET_ALL)
                self.runTraining(symbol)
        else:
            self.runTraining(quote)

    def runTraining(self, symbol):
        try:
            #start = datetime.now()
            #print(start.hour, ':', start.minute, ':', start.second, '.', start.microsecond)

            print("Retrieving Stock Data")
            data = oneMonthData.OneMonthData(symbol)

            features = data.features
            labels = data.labels

            print("Training Model on Data")

            trainedModel = model.Model(features, labels, data.currentData, symbol, LinearRegression)

            results = trainedModel.trainWithCrossVal()

            self.output["CrossVal Results"] = results
            stock = stockData.StockData(symbol)

            info = stock.info()

            self.output["CurrentPrice"] = info["previousClose"]
            self.output["Future Price"] = trainedModel.predictCurrentMonth()[0]

            self.output["Percent Increase"] = (trainedModel.predictCurrentMonth()[0]/info["previousClose"] - 1)*100
            print("Current Price: ", self.output["CurrentPrice"])
            print("Predicted Price: ", self.output["Future Price"])
            print("Predicted Percent Change in Price: ", self.output["Percent Increase"], "%")

            mse = results["test_mean_squared_error"]
            rootMSE = math.sqrt(mse)
            varianceScore = results["variance_score"]

            print("Error Margin: ", rootMSE)
            floor = self.output["Future Price"] - rootMSE
            ceiling = self.output["Future Price"] + rootMSE
            print("Predicted Floor: ", floor)
            print("Predicted Ceiling: ", ceiling)
            
            print("Variance Score: ", varianceScore)

            if floor > self.output["CurrentPrice"]:
                print(Fore.GREEN + "Predicted Gains GUARANTEED")
                print(Style.RESET_ALL)
            if ceiling < self.output["CurrentPrice"]:
                print(Fore.RED + "Predicted Losses GUARANTEED")
                print(Style.RESET_ALL)

            #end = datetime.now()
            #print(end.hour, ':', end.minute, ':', end.second, '.', end.microsecond)

            if self.printGraph:
                trainedModel.comparePredictions()
                if self.callback is not None:
                    self.callback()
        except Exception as e:
            print(e)
            if "Data doesn't exist for startDate" in str(e):
                print("This is a newer company")
            else:
                print(e)