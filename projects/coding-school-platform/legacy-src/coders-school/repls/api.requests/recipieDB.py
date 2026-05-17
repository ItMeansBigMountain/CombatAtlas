import requests
import json



# # key and value
# # {}  () [] "" ''

CodingClass = { # <--------- dictionary
  "key" : "value SHMALUE ",
  'teacher' : 'Affan ^_^  ',
  'PRICE' : 5.99,
  'students' : [ 'Jas' , 'Nal' , 1000 ], 
}




ingredients = 'apple'
dataBase_Link  = 'http://www.recipepuppy.com/api/?p=10&i='  + ingredients

dataCall = requests.get(  dataBase_Link   )
print(dataCall.text)
sample = json.loads(dataCall.text)  # converts string into dictionary

print( "Recipe: " + sample['results'][1]['title'] + " Ingredients: " + sample['results'][1]['ingredients'] )

# 