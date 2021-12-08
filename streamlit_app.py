from collections import namedtuple
import streamlit as st
import training.train as Train

"""
# Long Term Stock Prediction!
The following offers predictions of a chosen number months into the future to predict given a stock ticker.
"""
num_months = st.slider("Number of months into the future", 1, 11, 1)

Point = namedtuple('Point', 'x y')
data = []
train = Train.Train(quote='MSFT', printGraph=True, monthsLater=num_months)