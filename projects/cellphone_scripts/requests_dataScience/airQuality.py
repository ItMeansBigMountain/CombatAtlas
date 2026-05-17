import requests

# Mapping air polution data
# http://flothesof.github.io/world-air-quality-pollution-maps.html


# personal token (fareed320@gmail.com)
# https://aqicn.org/data-platform/token-confirm/4d7683ed-bafc-4344-9251-ff9fd3af607f



# get token from here https://aqicn.org/data-platform/token/#/
token = '689e622e12f429b46008d01876c128f81e0463ed'


city = input("Please enter city name ex: 'chicago' \n > ")
url = f'https://api.waqi.info/feed/{city}/?token={token}'



data = requests.get(url).json()
print(data)