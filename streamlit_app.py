from collections import namedtuple
import streamlit as st
from matplotlib import pyplot as plt

import training.train as Train

"""
# Long Term Stock Prediction!
The following offers predictions of a chosen number months into the future to predict given a stock ticker.
"""
num_months = st.slider("Number of months into the future", 1, 11, 1)
ticker = st.text_input("Ticker", "MSFT")
train = Train.Train(quote=ticker, printGraph=True, monthsLater=num_months, streamlit=True)
print("Printing Output")
st.write(train.output)