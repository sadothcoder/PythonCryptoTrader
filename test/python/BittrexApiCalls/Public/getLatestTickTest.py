
# Import Libraries
import requests
import decimal

# Setup
marketName = 'BTC-ETH'
period = 'oneMin'
url = 'https://bittrex.com/api/v2.0/pub/market/GetLatestTick?marketName={}&tickInterval={}'.format(marketName, period)

# Collect
response = requests.get(url)
print("Response status code: {}".format(response.status_code))
print("Latest tick for {} market".format(marketName))

# Display
DECIMAL_PLACES = decimal.Decimal(10) ** -8
for tick in response.json()['result']:
    result = ""
    result += "timestamp: {} \t".format(tick['T'])
    result += "open: {} \t".format(decimal.Decimal(tick['O']).quantize(DECIMAL_PLACES))
    result += "high: {} \t".format(decimal.Decimal(tick['H']).quantize(DECIMAL_PLACES))
    result += "low: {} \t".format(decimal.Decimal(tick['L']).quantize(DECIMAL_PLACES))
    result += "close: {} \t".format(decimal.Decimal(tick['C']).quantize(DECIMAL_PLACES))
    print(result)

