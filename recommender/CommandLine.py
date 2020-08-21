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
    sandp = input('Process Just S&P500? (Y/N)\n')
    processSANDP = False
    if sandp is "Y":
        processSANDP = True

    exportCSV = False
    outputToExcel = input('Output Results to CSV? (Y/N)\n')
    if outputToExcel is "Y":
        exportCSV = True

    print("Processing")
    train = Train.Train(printGraph=showGraph, useSAndP=processSANDP, outputExcel=exportCSV)
input('Press ENTER to exit\n')