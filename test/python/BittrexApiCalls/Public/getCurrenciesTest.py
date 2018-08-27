
# Import Libraries
import requests


# Support Functions
def extract_currency_data(currencyJson):
    for item in currencyJson['result']:
        currency = item['Currency']
        result = "\t"
        result += "Currency : {0:6} \t".format(currency)
        result += "Currency Long : {0:26} \t".format(item['CurrencyLong'])
        result += "MinConfirmation : {} \t".format(item['MinConfirmation'])
        result += "TxFee : {} \t".format(item['TxFee'])
        result += "IsActive : {} \t".format(item['IsActive'])
        result += "CoinType : {0:24} \t".format(item['CoinType'])
        result += "Notice : {0:50} \t".format(str(item['Notice']))
        result += "BaseAddress : {} \t".format(item['BaseAddress'])
        currencies[currency] = result


# Setup
url = 'https://bittrex.com/api/v2.0/pub/currencies/GetCurrencies?'


# Collect
response = requests.get(url)
print("Response status code: {}".format(response.status_code))


# Refine
json = response.json()
currencies = dict()
extract_currency_data(json)


# Display
print("Success : {}".format(json['success']))
print("Message : {}".format(json['message']))
print("Result : ")
for key in sorted(currencies.keys()):
    print(currencies[key])
