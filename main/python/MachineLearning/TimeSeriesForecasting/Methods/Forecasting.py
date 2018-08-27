
# Import libraries
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA
from pandas import Series

from main.python.MachineLearning.TimeSeriesForecasting.Methods.Stationarity import differencing_log, decomposing, \
    differencing_raw

import numpy as np
import matplotlib.pylab as pyplot
from matplotlib.pylab import rcParams
rcParams["figure.figsize"] = 15, 6


# =============================================
# =====     Autocorrelation functions     =====
# =============================================
def function_autocorrelation(ts_data, window_size):
    ts_log_diff = differencing_log(ts_data, window_size, False, False)
    lag_acf = acf(ts_log_diff, nlags=20)

    pyplot.plot(lag_acf)
    pyplot.axhline(y=0, linestyle="--", color="gray")
    pyplot.axhline(y=-1.96 / np.sqrt(len(ts_log_diff)), linestyle="--", color="gray")
    pyplot.axhline(y=1.96 / np.sqrt(len(ts_log_diff)), linestyle="--", color="gray")
    pyplot.title('Autocorrelation Function')


def function_partial_autocorrelation(ts_data, window_size):
    ts_log_diff = differencing_log(ts_data, window_size, False, False)
    lag_pacf = pacf(ts_log_diff, nlags=20, method="ols")

    pyplot.plot(lag_pacf)
    pyplot.axhline(y=0, linestyle="--", color="gray")
    pyplot.axhline(y=-1.96 / np.sqrt(len(ts_log_diff)), linestyle="--", color="gray")
    pyplot.axhline(y=1.96 / np.sqrt(len(ts_log_diff)), linestyle="--", color="gray")
    pyplot.title("Partial Autocorrelation Function")


# =========================================
# =====     ARIMA Model functions     =====
# =========================================
def model_ar(ts_data, window_size, should_plot=True):
    ts_log = np.log(ts_data)
    ts_log_diff = differencing_log(ts_data, window_size, False, False)
    model = ARIMA(ts_log, order=(1, 1, 0))
    results_AR = model.fit(disp=0)

    if should_plot:
        # root_mean_squared = sum((results_AR.fittedvalues - ts_log_diff) ** 2)
        pyplot.plot(ts_log_diff, color="blue", label="ts log difference")
        pyplot.plot(results_AR.fittedvalues, color="red", label="results AR fitted")
        pyplot.legend(loc="best")
        pyplot.title("Combined Model AR")
        # pyplot.title("RSS: {}".format(root_mean_squared))

    return results_AR


def model_ma(ts_data, window_size, should_plot=True):
    ts_log = np.log(ts_data)
    ts_log_diff = differencing_log(ts_data, window_size, False, False)
    model = ARIMA(ts_log, order=(0, 1, 1))
    results_MA = model.fit(disp=0)

    if should_plot:
        # root_mean_squared = sum((results_MA.fittedvalues - ts_log_diff) ** 2)
        pyplot.plot(ts_log_diff, color="blue", label="ts log difference")
        pyplot.plot(results_MA.fittedvalues, color="red", label="results MA fitted")
        pyplot.legend(loc="best")
        pyplot.title("Combined Model MA")
        # pyplot.title("RSS: {}".format(root_mean_squared))

    return results_MA


def model_combined(ts_data, window_size, should_plot=True):
    ts_log = np.log(ts_data)
    ts_log_diff = differencing_log(ts_data, window_size, False, False)
    model = ARIMA(ts_log, order=(1, 1, 1))
    results_ARIMA = model.fit(disp=0)

    if should_plot:
        # root_mean_squared = sum((results_MA.fittedvalues - ts_log_diff) ** 2)
        pyplot.plot(ts_log_diff, color="blue", label="ts log difference")
        pyplot.plot(results_ARIMA.fittedvalues, color="red", label="results ARIMA fitted")
        pyplot.legend(loc="best")
        pyplot.title("Combined Model AR-I-MA")
        # pyplot.title("RSS: {}".format(root_mean_squared))

    return results_ARIMA


def model_combined_no_log(ts_data, window_size, should_plot=True):
    ts_raw_diff = differencing_raw(ts_data, window_size, False, False)
    model = ARIMA(ts_data, order=(1, 1, 1))
    results_ARIMA = model.fit(disp=-1)

    if should_plot:
        # root_mean_squared = sum((results_MA.fittedvalues - ts_log_diff) ** 2)
        pyplot.plot(ts_data, color="blue", label="original")
        pyplot.plot(ts_raw_diff, color="red", label="differences")
        pyplot.plot(results_ARIMA.fittedvalues, color="green", label="results ARIMA fitted no logs")
        pyplot.legend(loc="best")
        pyplot.title("Combined Model AR-I-MA")
        # pyplot.title("RSS: {}".format(root_mean_squared))

    return results_ARIMA


# ===========================================================
# =====     Predictions using ARIMA Model functions     =====
# ===========================================================
def predictions(ts_data, window_size, should_plot=True):
    ts_log = np.log(ts_data)
    results_ARIMA = model_combined(ts_data, window_size, True)

    # Make a series with cumulative fitted values
    predictions_ARIMA_diff = Series(results_ARIMA.fittedvalues, copy=True)
    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()

    # Make a series with combined original and cumulative fitted values
    predictions_ARIMA_log = Series(ts_log.ix[0], index=ts_log.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum, fill_value=0)

    # predictions_ARIMA = np.exp(predictions_ARIMA_log)

    if should_plot:
        pyplot.figure(2)
        pyplot.plot(ts_data, color="blue", label="Original")
        # pyplot.plot(predictions_ARIMA, color="red", label="Pred Exponential")
        pyplot.plot(predictions_ARIMA_log, color="green", label="Prediction")
        pyplot.legend(loc="best")
        pyplot.title("Predictions")
        pyplot.show(block=False)


def predictions_better(ts_data, window_size, should_plot=True):
    results_ARIMA = model_combined_no_log(ts_data, window_size, True)

    # Make a series with cumulative fitted values
    predictions_ARIMA_diff = Series(results_ARIMA.fittedvalues, copy=True)
    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()

    # Make a series with combined original and cumulative fitted values
    predictions_ARIMA = Series(ts_data.ix[0], index=ts_data.index)
    # predictions_ARIMA = predictions_ARIMA.add(predictions_ARIMA_diff, fill_value=0)
    predictions_ARIMA = predictions_ARIMA.add(predictions_ARIMA_diff_cumsum, fill_value=0)

    if should_plot:
        pyplot.figure(2)
        pyplot.plot(ts_data, color="blue", label="Original")
        pyplot.plot(predictions_ARIMA, color="green", label="Prediction")
        pyplot.legend(loc="best")
        pyplot.title("Predictions")
        pyplot.show(block=False)
