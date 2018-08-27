
# Import Libraries
import requests


# Support Functions
def extract_market_data(json):
    for item in json['result']:
        market = item['MarketName']
        result = "\t"
        result += "MarketName : {} \t".format(market)
        result += "High : {0:8} \t".format(item['High'])
        result += "Low : {0:8} \t".format(item['Low'])
        result += "Volume : {0:8} \t".format(item['Volume'])
        result += "Last : {0:8} \t".format(item['Last'])
        result += "BaseVolume : {0:8} \t".format(item['BaseVolume'])
        result += "TimeStamp : {} \t".format(item['TimeStamp'])
        result += "Bid : {0:8} \t".format(item['Bid'])
        result += "Ask : {0:8} \t".format(item['Ask'])
        result += "OpenBuyOrders : {0:5} \t".format(item['OpenBuyOrders'])
        result += "OpenSellOrders : {0:5} \t".format(item['OpenSellOrders'])
        result += "PrevDay : {0:8} \t".format(item['PrevDay'])
        markets[market] = result


# Setup
# =======================================================================================================
# =======-> NOTE : // This one is a little messed up on V2.0 so use V1.1 it will look different <-=======
# =======================================================================================================
url = 'https://bittrex.com/api/v1.1/public/getMarketSummaries'


# Collect
response = requests.get(url)
print(response.status_code)
print("Market summaries")


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