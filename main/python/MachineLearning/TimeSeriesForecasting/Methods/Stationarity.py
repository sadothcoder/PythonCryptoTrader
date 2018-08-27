
# Import Libraries
import pandas as pd

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose

import numpy as np
import matplotlib.pylab as pyplot
from matplotlib.pylab import rcParams
rcParams["figure.figsize"] = 15, 6


def test_stationarity(ts_data, window_size, should_plot=True):
    # Use Dickey-Fuller testing on the time series to evaluate
    roll_mean = ts_data["ClosingPrice"].rolling(window=window_size).mean()
    roll_std = ts_data["ClosingPrice"].rolling(window=window_size).std()

    if should_plot:
        pyplot.figure(0)
        pyplot.plot(ts_data, color='blue', label='Original')
        pyplot.plot(roll_mean, color='red', label='Rolling Mean')
        pyplot.plot(roll_std, color='black', label='Rolling Std')
        pyplot.legend(loc='best')
        pyplot.title('Rolling Mean')
        pyplot.show(block=False)

    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(ts_data.unstack(), autolag="AIC")
    dfoutput = pd.Series(dftest[0:4], index=["Test Statistic", "p-value", "#Lags Used", "Number of Observations Used"])
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
    print(dfoutput)


# ====================================================
# =====     Estimating and eliminating trend     =====
# ====================================================
def movingAverage(ts_data, window_size):
    # Useful for seasonal stats like national park visitors
    ts_log = np.log(ts_data)
    ts_log_moving_avg = ts_log.rolling(window=window_size).mean()

    ts_log_moving_avg_diff = ts_log - ts_log_moving_avg
    ts_log_moving_avg_diff.dropna(inplace=True)
    test_stationarity(ts_log_moving_avg_diff, window_size)

    pyplot.plot(ts_log)
    pyplot.plot(ts_log_moving_avg, color="red")
    pyplot.show()


def exponentialWeighted(ts_data, window_size):
    # Useful for volatile stats like stock markets
    ts_log = np.log(ts_data)
    ts_log_exp_weighted_avg = ts_log.ewm(halflife=window_size).mean()
    ts_log_exp_weighted_avg_diff = ts_log - ts_log_exp_weighted_avg
    ts_log_exp_weighted_avg_diff.dropna(inplace=True)
    test_stationarity(ts_log_exp_weighted_avg_diff, window_size)

    pyplot.figure(1)
    pyplot.plot(ts_log)
    pyplot.plot(ts_log_exp_weighted_avg, color="red")
    pyplot.show()


# =====================================================
# =====     Eliminating trend and seasonality     =====
# =====================================================
def differencing_log(ts_data, window_size, should_plot_stationarity_test=True, should_plot=True):
    ts_log = np.log(ts_data)
    ts_log_diff = ts_log - ts_log.shift()
    ts_log_diff.dropna(inplace=True)

    test_stationarity(ts_log_diff, window_size, should_plot_stationarity_test)

    if should_plot:
        pyplot.figure(1)
        pyplot.plot(ts_log_diff)
        pyplot.show()

    return ts_log_diff


def differencing_raw(ts_data, window_size, should_plot_stationarity_test=True, should_plot=True):
    ts_diff = ts_data - ts_data.shift()
    ts_diff.dropna(inplace=True)

    test_stationarity(ts_diff, window_size, should_plot_stationarity_test)

    if should_plot:
        pyplot.figure(1)
        pyplot.plot(ts_diff)
        pyplot.show()

    return ts_diff


def decomposing(ts_data, window_size, should_plot_stationarity_test=True, should_plot=True):
    ts_log = np.log(ts_data)
    decomposition = seasonal_decompose(ts_log)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    ts_log_decomposition = residual
    ts_log_decomposition.dropna(inplace=True)

    test_stationarity(ts_log_decomposition, window_size, should_plot_stationarity_test)

    if should_plot:
        pyplot.figure(1)
        pyplot.subplot(411)
        pyplot.plot(ts_log, label="Original")
        pyplot.legend(loc="best")

        pyplot.subplot(412)
        pyplot.plot(trend, label="Trend")
        pyplot.legend(loc="best")

        pyplot.subplot(413)
        pyplot.plot(seasonal, label="Seasonality")
        pyplot.legend(loc="best")

        pyplot.subplot(414)
        pyplot.plot(residual, label="Residual")
        pyplot.legend(loc="best")
        pyplot.tight_layout()

    return trend
