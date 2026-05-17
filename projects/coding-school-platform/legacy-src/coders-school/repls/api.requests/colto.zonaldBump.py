import requests
import json
import random 

# GRAB the DATA
link = "https://api.adviceslip.com/advice"
data = requests.get(link).json()



# CREATING VARIABLES FROM DATA!
ad_visse = data['slip']['advice']



# PARSING THROUGH THE DATA
print( data.keys() )
print(ad_visse)
print( type   )
print(requests)





'''
NOTES!
everything in code is a variable...

STEP 1:
  grab the data

STEP 2:
  parse through the data 

STEP 3:
  create my variables!

'''