import training.train as Train

first_day = input('First day of month?\n')

if first_day == "N" or first_day == "n" or first_day == "no" or first_day == "No":
    train = Train.Train(printGraph=False, useSAndP=True, useRussell1000=False, outputExcel=True, monthsLater=1)
else:
    train = Train.Train(printGraph=False, useSAndP=True, useRussell1000=False, outputExcel=True, monthsLater=1)
    train2 = Train.Train(printGraph=False, useSAndP=True, useRussell1000=False, outputExcel=True, monthsLater=2)
    train4 = Train.Train(printGraph=False, useSAndP=True, useRussell1000=False, outputExcel=True, monthsLater=4)
    train8 = Train.Train(printGraph=False, useSAndP=True, useRussell1000=False, outputExcel=True, monthsLater=8)