# Import Libraries
from main.python.MachineLearning.TimeSeriesForecasting.CompoundingAverages.SupportFunctions import extract_data, collect_and_write_to_csv, extract_plot_data
from main.python.MachineLearning.TimeSeriesForecasting.CompoundingAverages.CompoundingAveragesModel import model

from matplotlib import pyplot


# ===== Setup =====
currency_from = "NZD"
currency_to = "USD"
interval = "1min"
api_key = "GRYVIVFOM0RKLZXP"

file_name = "MarketData-{}-{}-{}-interval.csv".format(currency_from, currency_to, interval)
collect_and_write_to_csv(currency_from, currency_to, interval, api_key, file_name)

# ===== Collect and prepare =====
data = extract_data(file_name)
timestamps, closing_prices = extract_plot_data(data)

# ===== Forecasting =====
predictions, outcomes = model(data)

# ===== Display =====
# Graph the actual data
pyplot.figure(0)
pyplot.plot(timestamps, closing_prices)

# Graph predictions vs outcomes
pyplot.figure(1)
index = range(len(predictions))
pyplot.plot(index, outcomes)
pyplot.plot(index, predictions)
pyplot.legend(["Outcomes", "Predictions"], loc='upper left')

pyplot.show()
