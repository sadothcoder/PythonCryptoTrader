
# Import Libraries
import requests

# Setup
url = 'https://bittrex.com/api/v2.0/pub/currencies/GetBTCPrice'

# Collect
response = requests.get(url)
print("Response status code: {}".format(response.status_code))

# Display
print(response.json()['result'])

