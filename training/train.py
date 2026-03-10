import os

import training.model as model
import data_retrieval.tickerSymbol as tickerSymbol
import data_retrieval.MonthLaterData as oneMonthData
from sklearn.linear_model import LinearRegression
import data_retrieval.stockData as stockData
import math
from colorama import Fore, Back, Style
from datetime import datetime
from datetime import date
import pandas as pd

# Only show "GUARANTEED" gains/losses when the model fit is strong enough to trust the band.
MIN_VARIANCE_SCORE_FOR_GUARANTEE = 0.5   # explained variance (higher = better fit)
MAX_ERROR_PCT_FOR_GUARANTEE = 15.0       # error margin as % of price (lower = tighter band)

class Train:
    def __init__(self, quote=None, printGraph=False, callback=None, outputExcel=False, useSAndP=False, useRussell1000=False, monthsLater=1, streamlit=False):
        self.output = {}
        self.printGraph = printGraph
        self.callback = callback
        self.outputExcel = outputExcel
        self.monthsLater = monthsLater
        self.streamlit = streamlit
        excel = pd.DataFrame(columns=['Symbol',
                                        'Current Price',
                                        'Future Price',
                                        'Percent Increase',
                                        'Error',
                                        'Error Percentage',
                                        'Floor',
                                        'Ceiling',
                                        'Variance Score'])
        if quote is None:
            ticker = tickerSymbol.TickerSymbols()
            symbols = ticker.symbols
            if useSAndP:
                symbols = ticker.sAndP
            elif useRussell1000:
                symbols = ticker.russell1000
            print(str(len(symbols)) + " total symbols")
            count = 0
            for symbol in symbols:
                print(Fore.YELLOW + "PROGRESS: ", count, len(symbols), (count/len(symbols)), monthsLater)
                print(Fore.BLUE + "Processing: ", symbol)
                print(Style.RESET_ALL)
                data = self.runTraining(symbol)
                if data is not None and outputExcel:
                    excel = pd.concat([excel, data])
                count = count + 1
            if outputExcel:
                currentDate = date.today()
                subDir = currentDate.strftime('%b %d %Y')
                outdir = f'../resources/Outputs/{subDir}/'
                print(f"Outputing to csv {outdir} {monthsLater}")
                if not os.path.exists(outdir):
                    os.mkdir(outdir)
                excel.to_csv(f"{outdir}Predictions {monthsLater}.csv")

        else:
            self.runTraining(quote)

    def _build_summary_frame(self, symbol, current_price, future_price, percent_increase, root_mse, error_percentage, floor, ceiling, variance_score):
        return pd.DataFrame(
            data=[[
                symbol,
                current_price,
                future_price,
                percent_increase,
                root_mse,
                error_percentage,
                floor,
                ceiling,
                variance_score,
            ]],
            columns=[
                'Symbol',
                'Current Price',
                'Future Price',
                'Percent Increase',
                'Error',
                'Error Percentage',
                'Floor',
                'Ceiling',
                'Variance Score',
            ],
        )

    def _log_results(self, symbol, root_mse, error_percentage, floor, ceiling, variance_score):
        print("Error Margin: ", root_mse)
        if error_percentage:
            print("Error Percentage: ", error_percentage)
        print("Predicted Floor: ", floor)
        print("Predicted Ceiling: ", ceiling)
        print("Variance Score: ", variance_score)

        current = self.output.get("CurrentPrice")
        if current is None:
            return

        high_confidence = (
            variance_score >= MIN_VARIANCE_SCORE_FOR_GUARANTEE
            and error_percentage <= MAX_ERROR_PCT_FOR_GUARANTEE
        )

        if high_confidence:
            if floor > current:
                print(Fore.GREEN + "Predicted Gains GUARANTEED")
                print(Style.RESET_ALL)
                self.output["Message"] = "Predicted GAINS Highly Likely given Error values"
            elif ceiling < current:
                print(Fore.RED + "Predicted Losses GUARANTEED")
                print(Style.RESET_ALL)
                self.output["Message"] = "Predicted LOSSES Highly Likely given Error values"

    def runTraining(self, symbol):
        try:
            print("Retrieving Stock Data")
            data = oneMonthData.MonthLaterData(symbol, monthsLater=self.monthsLater)

            features = data.features
            labels = data.labels

            print("Training Model on Data")
            trainedModel = model.Model(features, labels, data.currentData, symbol, LinearRegression)
            print("Model Trained")

            results = trainedModel.trainWithCrossVal()
            self.output["CrossVal Results"] = results

            stock = stockData.StockData(symbol)
            previous_close = stock.previous_close()
            prediction = trainedModel.predictCurrentMonth()[0]

            self.output["CurrentPrice"] = previous_close
            self.output["Future Price"] = prediction
            self.output["Percent Increase"] = 0

            if previous_close is not None and previous_close > 0:
                self.output["Percent Increase"] = (prediction / previous_close - 1) * 100

            print("Current Price: ", self.output["CurrentPrice"])
            print("Predicted Price: ", self.output["Future Price"])
            print("Predicted Percent Change in Price: ", self.output["Percent Increase"], "%")

            mse = results["test_mean_squared_error"]
            root_mse = math.sqrt(mse)
            variance_score = results["variance_score"]

            error_percentage = 0
            if self.output["CurrentPrice"] is not None and self.output["CurrentPrice"] > 0:
                error_percentage = (root_mse / self.output["CurrentPrice"]) * 100

            floor = self.output["Future Price"] - root_mse
            ceiling = self.output["Future Price"] + root_mse

            self._log_results(symbol, root_mse, error_percentage, floor, ceiling, variance_score)

            if self.printGraph:
                trainedModel.comparePredictions(streamlit=self.streamlit)
                if self.callback is not None:
                    self.callback()

            return self._build_summary_frame(
                symbol,
                self.output["CurrentPrice"],
                self.output["Future Price"],
                self.output["Percent Increase"],
                root_mse,
                error_percentage,
                floor,
                ceiling,
                variance_score,
            )
        except Exception as e:
            print(e)
            if "Data doesn't exist for startDate" in str(e):
                print("This is a newer company")
            else:
                print(e)