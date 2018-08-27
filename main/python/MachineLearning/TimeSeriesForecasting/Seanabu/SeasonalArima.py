
# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.seasonal import seasonal_decompose

from main.python.MachineLearning.TimeSeriesForecasting.Seanabu.supportMethods import test_stationarity


# Collect Data

df = pd.read_csv('portland-oregon-average-monthly-.csv', index_col=0)
df.index.name = None
df.reset_index(inplace=True)
df.drop(df.index[114], inplace=True)

# Transform to make usable
start = datetime.datetime.strptime("1973-01-01", "%Y-%m-%d")
date_list = [start + relativedelta(months=x) for x in range(0, 114)]
df['index'] = date_list
df.set_index(['index'], inplace=True)
df.index.name = None
df.columns = ['riders']
df['riders'] = df.riders.apply(lambda x: int(x) * 100)

# Test plot
df.riders.plot(figsize=(12, 8), title='Monthly Ridership', fontsize=14)

# Decompose it
decomposition = seasonal_decompose(df.riders, freq=12)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid
ts_log_decomposition = residual
ts_log_decomposition.dropna(inplace=True)

plt.figure(1)
plt.subplot(411)
plt.plot(df.riders, label="Original")
plt.legend(loc="best")

plt.subplot(412)
plt.plot(trend, label="Trend")
plt.legend(loc="best")

plt.subplot(413)
plt.plot(seasonal, label="Seasonality")
plt.legend(loc="best")

plt.subplot(414)
plt.plot(residual, label="Residual")
plt.legend(loc="best")
plt.tight_layout()


test_stationarity(df.riders, 12)

plt.show()
