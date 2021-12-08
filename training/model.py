import pandas as pd
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
import matplotlib.pyplot as plt
from sklearn.metrics import explained_variance_score, max_error, mean_squared_error
from sklearn.model_selection import train_test_split, cross_validate
import streamlit as st

class Model:
    def __init__(self, featureData, labelData, currentMonthData, quote='MFST', classifier=LinearRegression):
        self.features = featureData
        self.labels = labelData['finalPrice']
        self.quote = quote
        self.currentMonth = currentMonthData
        self.classifier = classifier

    def train(self):
        self.clf = self.classifier()
        self.clf.fit(self.features, self.labels)

    def trainWithCrossVal(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.features, self.labels,
                                                                                test_size=0.25, random_state=0)
        self.clf = self.classifier()
        results = cross_validate(self.clf, self.features, self.labels, cv=7, verbose=1,
                           scoring=['explained_variance', 'max_error', "neg_mean_squared_error"], n_jobs=-1)
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