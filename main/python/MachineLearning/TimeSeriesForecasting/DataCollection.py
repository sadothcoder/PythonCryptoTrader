# Import Libraries
from requests import get
from csv import DictWriter
from decimal import Decimal


def collectAndWriteToCsv(marketName, period, fileName):

    # Setup
    url = 'https://bittrex.com/api/v2.0/pub/market/getTicks?marketName={}&tickInterval={}'.format(marketName, period)
    decimalPlaces = Decimal(10) ** -8

    # Collect
    response = get(url)
    print("Response status code: {}".format(response.status_code))


    # Write to file
    with open(fileName, "w", newline="") as csvfile:
        fieldNames = ["TimeStamp", "ClosingPrice"]
        writer = DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()

        for tick in response.json()["result"]:
            writer.writerow({"TimeStamp": tick["T"][0:10], "ClosingPrice": Decimal(tick["C"]).quantize(decimalPlaces)})