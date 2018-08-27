
# Import Libraries
import requests

# Setup
url = 'https://socket.bittrex.com/signalr/ping?'

# Collect
response = requests.get(url)
print("Response status code: {}".format(response.status_code))

# Display
print(response.json()['Response'])

