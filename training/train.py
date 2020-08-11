import pandas as pd
import training.model as model
import data_retrieval.tickerSymbol as tickerSymbol
import data_retrieval.OneMonthData as oneMonthData
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
import data_retrieval.stockData as stockData


class Train:
    def __init__(self, quote=None):
        ticker = tickerSymbol.TickerSymbols()
        print(str(len(ticker.symbols)) + " total symbols")
        if quote is None:
            for symbol in ticker.symbols:
                self.runTraining(symbol)
        else:
            self.runTraining(quote)


    def runTraining(self, symbol):
        try:
            print(symbol)
            data = oneMonthData.OneMonthData(symbol)

            features = data.features
            labels = data.labels

            #print(features.tail())
            #print(labels.tail())

            trainedModel = model.Model(features, labels, data.currentData, symbol, LinearRegression)
            results = trainedModel.trainWithCrossVal()
            print(results)
            stock = stockData.StockData(symbol)
            info = stock.info()

            # Determine if there will be a guaranteed profit if the stock is bought now
            print(info["previousClose"])
            print(trainedModel.predictCurrentMonth())
            trainedModel.comparePredictions()
        except Exception as e:
            print("This is either a newer company or some sort of error occured")
            if "Data doesn't exist for startDate":
                print("This is a newer company")
            else:
                print(e)