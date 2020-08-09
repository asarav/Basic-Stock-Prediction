import pandas as pd
import training.model as model
import data_retrieval.tickerSymbol as tickerSymbol
import data_retrieval.OneMonthData as oneMonthData

tickerSymbol = tickerSymbol.TickerSymbols()
print(str(len(tickerSymbol.symbols)) + " total symbols")
oneMonthData = oneMonthData.OneMonthData(tickerSymbol.symbols[0])

features = oneMonthData.features
labels = oneMonthData.labels

print(features.tail())
print(labels.tail())

model = model.Model(features, labels, oneMonthData.currentData, tickerSymbol.symbols[0])
results = model.trainWithCrossVal()
print(results)
model.comparePredictions()
print(model.predictCurrentMonth())