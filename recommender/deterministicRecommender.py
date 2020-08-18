import training.train as Train

# Generate a Buy or Sell Recommendation based on current properties of the stock

ticker = input('Enter Stock Ticker\n')
train = Train.Train(quote=ticker, printGraph=True)