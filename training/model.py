import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import explained_variance_score, max_error, mean_squared_error
from sklearn.model_selection import cross_validate, TimeSeriesSplit
import streamlit as st

class Model:
    def __init__(self, featureData, labelData, currentMonthData, quote='MSFT', classifier=LinearRegression):
        self.features = featureData
        self.labels = labelData['finalPrice']
        self.quote = quote
        self.currentMonth = currentMonthData
        self.classifier = classifier

    def train(self):
        self.clf = self.classifier()
        self.clf.fit(self.features, self.labels)

    def trainWithCrossVal(self):
        # ensure chronological ordering for time-series data
        features = self.features.sort_index()
        labels = self.labels.loc[features.index]

        # chronological hold-out: last 25% of observations as test set
        test_size = int(len(features) * 0.25)
        if test_size == 0:
            raise ValueError("Not enough data points to create a time-series test split.")

        self.X_train = features.iloc[:-test_size]
        self.X_test = features.iloc[-test_size:]
        self.y_train = labels.iloc[:-test_size]
        self.y_test = labels.iloc[-test_size:]

        self.clf = self.classifier()
        # time-series aware cross-validation
        tscv = TimeSeriesSplit(n_splits=7)
        results = cross_validate(
            self.clf,
            features,
            labels,
            cv=tscv,
            verbose=1,
            scoring=['explained_variance', 'max_error', "neg_mean_squared_error"],
            n_jobs=-1
        )
        self.clf.fit(self.X_train, self.y_train)
        test_predictions = self.clf.predict(self.X_test)

        testExplainedVarianceScore = explained_variance_score(self.y_test, test_predictions)
        testMaxError = max_error(self.y_test, test_predictions)
        testMeanSquaredError = mean_squared_error(self.y_test, test_predictions)

        test_results = { 'variance_score': testExplainedVarianceScore,
                         'test_max_error': testMaxError,
                         'test_mean_squared_error': testMeanSquaredError,
                         'crossValResults': results
                       }
        return test_results

    def comparePredictions(self, streamlit=False):
        predictions = self.clf.predict(self.features)

        plt.plot(self.labels.values, label="Labels", marker='o')
        plt.plot(predictions, label="Predictions", marker='o')
        plt.legend(loc="upper left")
        plt.title('Labels vs Predictions for ' + self.quote)
        if not streamlit:
            plt.show()
        else:
            fig = plt.gcf()
            st.pyplot(fig)

    def predictCurrentMonth(self):
        predictions = self.clf.predict(self.currentMonth)
        return predictions