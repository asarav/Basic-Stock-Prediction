import training.train as Train

# main.py
numberOfMonths = int(input("Choose Number of Months into the future to predict (Must be less than 12)\n"))
all = input('Process all Stock Tickers? (Y/N)\n')
displayGraph = input('Display Graph? (Y/N)\n')
showGraph = False
if displayGraph == "Y" or displayGraph == "y":
    showGraph = True
if all == "N" or all == "n":
    ticker = input('Enter Stock Ticker\n')
    print("Processing")
    train = Train.Train(quote=ticker, printGraph=showGraph, monthsLater=numberOfMonths)
else:
    sandp = input('Process Just S&P500? (Y/N)\n')
    processSANDP = False
    processRussell1000 = False
    if sandp == "Y" or sandp == "y":
        processSANDP = True
    else:
        russell1000 = input('Process Just Russell 1000? (Y/N)\n')
        if russell1000 == "Y" or russell1000 == "y":
            processRussell1000 = True

    exportCSV = False
    outputToExcel = input('Output Results to CSV? (Y/N)\n')
    if outputToExcel == "Y" or outputToExcel == "y":
        exportCSV = True

    print("Processing")
    train = Train.Train(printGraph=showGraph, useSAndP=processSANDP, useRussell1000=processRussell1000, outputExcel=exportCSV, monthsLater=numberOfMonths)
input('Press ENTER to exit\n')