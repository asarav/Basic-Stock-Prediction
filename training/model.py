import pandas as pd
from sklearn import svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

class Model:
    def __init__(self, featureData, labelData):
        self.features = featureData
        self.labels = labelData['finalPrice']

    def train(self):
        self.clf = LinearRegression()
        self.clf.fit(self.features, self.labels)

    def comparePredictions(self):
        predictions = self.clf.predict(self.features)
        plt.plot(self.labels.values)
        plt.plot(predictions)
        plt.title('Labels vs Predictions')
        plt.show()

    def predictCurrentMonth(self):
        return