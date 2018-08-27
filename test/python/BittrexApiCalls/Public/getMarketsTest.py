
# Import Libraries
import requests


# Support Functions
def extract_market_data(json):
    for item in json['result']:
        market = item['MarketName']
        result = "\t"
        result += "MarketName : {} \t".format(market)
        result += "MarketCurrency : {} \t".format(item['MarketCurrency'])
        result += "BaseCurrency : {0:4} \t".format(item['BaseCurrency'])
        result += "MarketCurrencyLong : {0:28} \t".format(item['MarketCurrencyLong'])
        result += "BaseCurrencyLong : {0:10} \t".format(item['BaseCurrencyLong'])
        result += "MinTradeSize : {0:12} \t".format(str(item['MinTradeSize']))
        result += "IsActive : {} \t".format(item['IsActive'])
        result += "Created : {} \t".format(item['Created'])
        markets[market] = result


# Setup
# =======================================================================================================
# =======-> NOTE : // This one is a little messed up on V2.0 so use V1.1 it will look different <-=======
# =======================================================================================================
url = 'https://bittrex.com/api/v1.1/public/getmarkets?'


# Collect
response = requests.get(url)


# Refine
marketJson = response.json()
markets = dict()
extract_market_data(marketJson)


# Display
print("Success : {}".format(marketJson['success']))
print("Message : {}".format(marketJson['message']))
print("Result : ")
for key in sorted(markets.keys()):
    print(markets[key])
