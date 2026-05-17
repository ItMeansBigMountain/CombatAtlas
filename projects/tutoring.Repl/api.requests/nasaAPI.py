import requests
import json

apiKey = 'YOUR_NASA_API_KEY'

def MarsRover_pics():
  url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=' + apiKey
  dataCall = requests.get(url)
  convert_Dict = json.loads(dataCall.text)
  photosList = convert_Dict['photos'] 

  All_Links = []
  for x in photosList:
    All_Links.append(x['img_src'])

  return All_Links



def NASA_allPages():
  search = input("What would you like to search for? ")

  output =[]
  page = 1
  while True:
    url = 'https://images-api.nasa.gov/search?page=' + str(page) + '&q=' + search
    dataCall = requests.get(url)
    convert_Dict = json.loads(dataCall.text)
    if len(convert_Dict['collection']['items']) == 0:
      break
    for x in convert_Dict['collection']['items']:
      if 'links' in x:
        print(x['links'][0]['href']) 
        output.append(x['links'][0]['href'])
    page = page + 1


  print('{} results...'.format(len(output)))
  return output



def NASA_page1():
  search = input("What would you like to search for? ")

  output =[]
  page = 1
  while True:
    url = 'https://images-api.nasa.gov/search?page=' + str(page) + '&q=' + search
    dataCall = requests.get(url)
    convert_Dict = json.loads(dataCall.text)
    if len(convert_Dict['collection']['items']) == 0:
      break
    for x in convert_Dict['collection']['items']:
      if 'links' in x:
        print(x['links'][0]['href']) 
        output.append(x['links'][0]['href'])
    page = page + 1


    # FLOODGATES remove for all pages
    break


  print('{} results...'.format(len(output)))
  return output







def main():
  print("Welcome to the solar system!")
  print('1 : Mars Rover')

  option = input('\nWhat would you like to choose? ')

  if int(option) == 1:
    rover = MarsRover_pics()
    print(rover)
    



# calling functions down here
NASA_allPages()


