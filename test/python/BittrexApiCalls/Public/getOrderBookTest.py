
# Import Libraries
import requests


# Setup
# =======================================================================================================
# =======-> NOTE : // This one is a little messed up on V2.0 so use V1.1 it will look different <-=======
# =======================================================================================================
marketName = "ETH-LTC"
marketType = "both" # can be buy/sell/both
url = 'https://bittrex.com/api/v1.1/public/getOrderBook?market={}&type={}'.format(marketName, marketType)


# Collect
responseJson = requests.get(url).json()


# Display
print("Order book for {} with {} record types".format(marketName, marketType))
print("Success : {}".format(responseJson['success']))
print("Message : {}".format(responseJson['message']))
print("Result : ")

print("\tBuying --\n")
for sale in responseJson['result']['buy']:
    for line in sale:
        print("\t\t{} : {}".format(line, sale[line]))
    print()

print("\tSelling --\n")
for sale in responseJson['result']['sell']:
    for line in sale:
        print("\t\t{} : {}".format(line, sale[line]))
    print()
