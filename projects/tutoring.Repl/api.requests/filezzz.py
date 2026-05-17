import requests
import json
import pprint
import time

# go to this website and grab all the info on the page
#data = requests.get("https://api.adviceslip.com/advice")

#since the website was an api website, they returned us data in json format
# this means that we need to convert the data.text into a Dictionary
#dataDictionary = json.loads(data.text)

# now that we have a dictionary, we need to specify what we are looking for inside of it...
    #sample = dataDictionary['slip']['advice'] 
# slip is the outer dictionary key
# advice is the inner dictionary key
# printing sample is returning the value of advice
try:
  saveFile = open('list.txt', 'a', encoding="utf-8")
  for i in range(0,201):
    time.sleep(1)
    data = requests.get("https://api.adviceslip.com/advice")
    dataDictionary = json.loads(data.text)
    sample = dataDictionary['slip']['advice']
    saveFile.write(sample)
    saveFile.write("\n")
  saveFile.close()
except Exception as e:
  saveFile.close()
  print(e)