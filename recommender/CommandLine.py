import training.train as Train

# main.py
all = input('Process all Stock Tickers? (Y/N)\n')
displayGraph = input('Display Graph? (Y/N)\n')
showGraph = False
if displayGraph is "Y":
    showGraph = True
if all is "N":
    ticker = input('Enter Stock Ticker\n')
    print("Processing")
    train = Train.Train(quote=ticker, printGraph=showGraph)
else:
    print("Processing")
    train = Train.Train(printGraph=showGraph)
input('Press ENTER to exit\n')