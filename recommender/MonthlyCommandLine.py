import training.train as Train

first_day = input('First day of month?\n')

if first_day == "N" or first_day == "n" or first_day == "no" or first_day == "No":
    train = Train.Train(printGraph=False, useSAndP=True, useRussell1000=False, outputExcel=True, monthsLater=1)
    print("Completed")
else:
    print("Processing 1 month")
    train = Train.Train(printGraph=False, useSAndP=True, useRussell1000=False, outputExcel=True, monthsLater=1)
    print("Processing 2 months")
    train2 = Train.Train(printGraph=False, useSAndP=True, useRussell1000=False, outputExcel=True, monthsLater=2)
    print("Processing 4 months")
    train4 = Train.Train(printGraph=False, useSAndP=True, useRussell1000=False, outputExcel=True, monthsLater=4)
    print("Processing 8 months")
    train8 = Train.Train(printGraph=False, useSAndP=True, useRussell1000=False, outputExcel=True, monthsLater=8)
    print("Completed")