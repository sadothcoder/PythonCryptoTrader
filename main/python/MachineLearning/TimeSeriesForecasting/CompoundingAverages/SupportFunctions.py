# Import Libraries
from requests import get
from csv import DictWriter
from decimal import Decimal
import csv
from matplotlib.pylab import rcParams

rcParams["figure.figsize"] = 15, 6


def determine_trend(open, close, high, low):
    actual_mid_point = (open + close) / 2
    trend_mid_point = (high + low) / 2
    return trend_mid_point > actual_mid_point


def collect_and_write_to_csv(currency_from, currency_to, interval, api_key, file_name):
    # Setup
    url = "https://www.alphavantage.co/query?function=FX_INTRADAY&"
    # url = "https://www.alphavantage.co/query?function=FX_DAILY&"
    url += "from_symbol={}&".format(currency_from)
    url += "to_symbol={}&".format(currency_to)
    url += "interval={}&".format(interval)
    url += "outputsize=full&apikey={}".format(api_key)
    decimal_places = Decimal(10) ** -8

    # Collect
    response = get(url).json()

    # Write to file
    with open(file_name, "w", newline="") as csvfile:
        field_names = ["Timestamp", "Open", "High", "Low", "Close", "Difference", "Stagnated", "Increased", "Decreased", "Trending Up", "Trending Down"]
        writer = DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        timeseries = response["Time Series FX ({})".format(interval)]

        for tick in timeseries.items():
            timestamp = tick[0]
            values = tick[1]
            open_value = Decimal(values["1. open"]).quantize(decimal_places)
            high_value = Decimal(values["2. high"]).quantize(decimal_places)
            low_value = Decimal(values["3. low"]).quantize(decimal_places)
            close_value = Decimal(values["4. close"]).quantize(decimal_places)

            difference = (close_value - open_value).quantize(decimal_places)
            if close_value == open_value:
                difference = 0

            increased = 0
            if close_value > open_value:
                increased = 1

            decreased = 0
            if close_value < open_value:
                decreased = 1

            stagnated = 0
            if (increased + decreased) == 0:
                stagnated = 1

            trend_up = 0
            trend_down = 0
            if determine_trend(open_value, close_value, high_value, low_value):
                trend_up = 1
            else:
                trend_down = 1

            writer.writerow({"Timestamp": timestamp,
                             "Open": open_value,
                             "High": high_value,
                             "Low": low_value,
                             "Close": close_value,
                             "Difference": difference,
                             "Stagnated": stagnated,
                             "Increased": increased,
                             "Decreased": decreased,
                             "Trending Up": trend_up,
                             "Trending Down": trend_down})


def extract_data(file_name):
    data = []
    with open(file_name, newline='') as csv_file:
        spamreader = csv.reader(csv_file, delimiter=',', quotechar='\"')
        first = True
        for row in spamreader:
            if first:
                first = False
            else:
                values = [row[0],
                          float(row[1]),
                          float(row[2]),
                          float(row[3]),
                          float(row[4]),
                          float(row[5]),
                          int(row[6]),
                          int(row[7]),
                          int(row[8]),
                          int(row[9]),
                          int(row[10])]
                data.insert(0, values)
    return data


def extract_plot_data(data):
    x_data = []
    y_data = []
    counter = 1
    for row in data:
        x_data.append(counter)
        y_data.append(row[4])
        counter += 1
    return x_data, y_data
