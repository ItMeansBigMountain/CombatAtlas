import requests
import json

data = requests.get('https://api.adviceslip.com/advice')

adviceText = json.loads(Request.text)
sample = adviceText["slip"]["advice"]
print(sample)


