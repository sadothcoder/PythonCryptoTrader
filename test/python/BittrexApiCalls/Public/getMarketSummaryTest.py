
# Import Libraries
import requests


# Setup
# =======================================================================================================
# =======-> NOTE : // This one is a little messed up on V2.0 so use V1.1 it will look different <-=======
# =======================================================================================================
marketName = "ETH-LTC"
url = 'https://bittrex.com/api/v1.1/public/getMarketSummary?market={}'.format(marketName)


# Collect
response = requests.get(url)
print(response.status_code)


# Refine
marketJson = response.json()
markets = dict()


# Display
print("Success : {}".format(marketJson['success']))
print("Message : {}".format(marketJson['message']))
print("Result : ")
for item in marketJson['result']:
    for i in item:
        print("\t{:15} : {}".format(i, item[i]))
