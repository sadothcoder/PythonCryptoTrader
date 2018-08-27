
# Import Libraries
from pandas import read_csv

from main.python.MachineLearning.TimeSeriesForecasting.DataCollection import collectAndWriteToCsv
from main.python.MachineLearning.TimeSeriesForecasting.Methods.Forecasting import function_autocorrelation, \
    function_partial_autocorrelation, model_ma, model_ar, model_combined, predictions, predictions_better
from main.python.MachineLearning.TimeSeriesForecasting.Methods.MultipleSplits import method_multipleSplits
from main.python.MachineLearning.TimeSeriesForecasting.Methods.SlidingWindow import method_slidingWindow
from main.python.MachineLearning.TimeSeriesForecasting.Methods.Stationarity import test_stationarity, movingAverage, \
    exponentialWeighted, differencing_log, decomposing, differencing_raw

from matplotlib import pyplot


# Setup
market_name = "ETH-LTC"
trade_period = "day"
file_name = "MarketData.csv"
window_size = 10
print("Recent closing prices for {} exchange".format(market_name))
collectAndWriteToCsv(market_name, trade_period, file_name)


# Collect and prepare
data = read_csv(file_name, parse_dates=["TimeStamp"], index_col="TimeStamp")
# method_multipleSplits(3, file_name)
# method_slidingWindow(100, file_name)

# ===== Stationarity =====
test_stationarity(data, window_size)
# movingAverage(data, window_size)
# exponentialWeighted(data, window_size)
# ts_log_diff = differencing_log(data, window_size)
# ts_raw_diff = differencing_raw(data, window_size)
# ts_log_decompose = decomposing(data, window_size)

# ===== Forecasting =====
# function_autocorrelation(data, window_size)
# function_partial_autocorrelation(data, window_size)
# model_ar(data, window_size)
# model_ma(data, window_size)
model_combined(data, window_size)
# predictions(data, window_size)
predictions_better(data, window_size)

# Display
# pyplot.plot(data)
pyplot.show()
