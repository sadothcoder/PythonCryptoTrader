
# Clearly this method would not work for time series evaluation
# This was just here to see more how it would handle the situation

# Import Libraries
import numpy as np
import matplotlib.pylab as pyplot
import pandas as pd

from main.python.MachineLearning.TimeSeriesForecasting.DataCollection import collectAndWriteToCsv

from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression


# Setup
market_name = "ETH-LTC"
trade_period = "day"
file_name = "MarketData.csv"
window_size = 10
print("Recent closing prices for {} exchange".format(market_name))
collectAndWriteToCsv(market_name, trade_period, file_name)


# Import the dataset
series = pd.read_csv(file_name)
x_data = series.index.values.reshape(-1, 1)
y_data = series["ClosingPrice"].values


# Splitting the data into the Training and Test sets
num_splits = 2
splits = TimeSeriesSplit(n_splits=num_splits)

index = 1
for train_index, test_index in splits.split(x_data):
    x_train, x_test = x_data[train_index], x_data[test_index]
    y_train, y_test = y_data[train_index], y_data[test_index]

    # Fitting the regressor
    regressor = LinearRegression()
    regressor.fit(x_train, y_train)

    pyplot.figure(index)
    pyplot.subplot(211)
    pyplot.plot(x_train, y_train, color="red", label="Original")
    pyplot.plot(x_train, regressor.predict(x_train), color="blue", label="Prediction")
    pyplot.legend(loc="best")
    pyplot.title("Training data - {}".format(index))

    pyplot.figure(index)
    pyplot.subplot(212)
    pyplot.plot(x_test, y_test, color="red", label="Original")
    pyplot.plot(x_test, regressor.predict(x_test), color="blue", label="Prediction")
    pyplot.legend(loc="best")
    pyplot.title("Test data - {}".format(index))

    index += 1

pyplot.show()
