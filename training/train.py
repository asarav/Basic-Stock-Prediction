import pandas as pd
import training.model as model
import data_retrieval.tickerSymbol as tickerSymbol
import data_retrieval.OneMonthData as oneMonthData

ticker = tickerSymbol.TickerSymbols()
print(str(len(ticker.symbols)) + " total symbols")
for symbol in ticker.symbols:
    try:
        print(symbol)
        data = oneMonthData.OneMonthData(symbol)

        features = data.features
        labels = data.labels

        #print(features.tail())
        #print(labels.tail())

        trainedModel = model.Model(features, labels, data.currentData, symbol)
        results = trainedModel.trainWithCrossVal()
        print(results)
        trainedModel.comparePredictions()
        print(trainedModel.predictCurrentMonth())
    except:
        print("This is either a newer company or some sort of error occured")