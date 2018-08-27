
# Import Libraries
import requests
import decimal

# Setup
market_name = 'USD-BTC'
period = 'day'
url = 'https://bittrex.com/api/v2.0/pub/market/getTicks?marketName={}&tickInterval={}'.format(market_name, period)

# Collect
response = requests.get(url)
print("Response status code: {}".format(response.status_code))

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

