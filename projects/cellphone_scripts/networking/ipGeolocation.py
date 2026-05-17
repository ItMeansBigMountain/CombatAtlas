import requests #lets us request a http response
import json #convert response strings into progromatic data


ipAddress = input('Please enter IP Address: ')

Request = requests.get('https://api.ipgeolocation.io/ipgeo?apiKey=edd9fcebb3904262b8f344f8e94c084f&ip='+ ipAddress +'&fields=city&output=json')

sample = json.loads(Request.text)

print(sample) #not free anymore

# print('Ip Address: {}'.format(sample['ip']))
# print('City: {}'.format(sample['city']))