
# Import Libraries
import requests
import decimal


# Support Functions
def extract_market_data(json):
    for item in json['result']:
        result = "\t"
        result += "OrderType : {0:10} \t".format(item['OrderType'])
        result += "Id : {} \t".format(item['Id'])
        result += "TimeStamp : {0:30} \t".format(item['TimeStamp'])
        result += "Quantity : {} \t".format(decimal.Decimal(item['Quantity']).quantize(DECIMAL_PLACES))
        result += "Price : {} \t".format(decimal.Decimal(item['Price']).quantize(DECIMAL_PLACES))
        result += "Total : {} \t".format(decimal.Decimal(item['Total']).quantize(DECIMAL_PLACES))
        result += "FillType : {0:16} \t".format(item['FillType'])
        marketHistory[item['Id']] = result


# Setup
# =======================================================================================================
# =======-> NOTE : // This one is a little messed up on V2.0 so use V1.1 it will look different <-=======
# =======================================================================================================
marketName = "ETH-LTC"
url = 'https://bittrex.com/api/v1.1/public/getMarketHistory?market={}'.format(marketName)
DECIMAL_PLACES = decimal.Decimal(10) ** -8


# Collect
marketJson = requests.get(url).json()
marketHistory = dict()
extract_market_data(marketJson)


# Display
print("Success : {}".format(marketJson['success']))
print("Message : {}".format(marketJson['message']))
print("Result : ")
for key in sorted(marketHistory.keys()):
    print(marketHistory[key])
