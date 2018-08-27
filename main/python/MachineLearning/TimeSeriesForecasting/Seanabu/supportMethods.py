
# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

def test_stationarity(ts_data, window_size):
    # Use Dickey-Fuller testing on the time series to evaluate
    roll_mean = ts_data.rolling(window=window_size).mean()
    roll_std = ts_data.rolling(window=window_size).std()

    plt.figure(0)
    plt.plot(ts_data, color='blue', label='Original')
    plt.plot(roll_mean, color='red', label='Rolling Mean')
    plt.plot(roll_std, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean')
    plt.show(block=False)

    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(ts_data, autolag="AIC")
    dfoutput = pd.Series(dftest[0:4], index=["Test Statistic", "p-value", "#Lags Used", "Number of Observations Used"])
    for key, value in dftest[4].items():
        dfoutput["Critical Value (%s)" % key] = value
    print(dfoutput)
