# from core.models import Workout

# from core.serializers import WorkoutSerializer
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser

"""




# MANUALLY ADDING OBJECTS TO SQLite3

a = Article(title = "testing" , author = "affan" , email = "a.test@lol.com"  )
a.save()
b = Article(title = "b" , author = "affan" , email = "b.test@lol.com"  )
b.save()




# CONVERTING DB OBJECT INTO PYTHON OBJECT

serializer = ArticleSerializer(a)  # single model object

serializer.data
{'title': 'testing', 'author': 'affan', 'email': 'a.test@lol.com', 'date': '2022-03-20T17:35:21.665060Z'} #dict

content = JSONRenderer().render(serializer.data)

content
b'{"title":"testing","author":"affan","email":"a.test@lol.com","date":"2022-03-20T17:35:21.665060Z"}' #json













# CONVERTING DB OBJECT INTO PYTHON OBJECT

serializer = ArticleSerializer(Article.objects.all() , many = True) # all objects of model

serializer.data
[OrderedDict([('title', 'testing'), ('author', 'affan'), ('email', 'a.test@lol.com'), ('date', '2022-03-20T17:35:21.665060Z')]), OrderedDict([('title', 'b'), ('author', 'affan'), ('email', 'b.test@lol.com'), ('date', '2022-03-20T17:40:23.009135Z')])]











# MANUALLY POSTING WORKOUTS
import requests
import json


url = 'http://127.0.0.1:8000/api/'

f = open("workouts.json" , "r")
workouts_JSON = json.loads( f.read() )
f.close()


for key in workouts_JSON:
    for x in range( 0 , len(workouts_JSON[key]) , 1):
        myobj = {
            "title" : workouts_JSON[key][x][0] , 
            "description" : "testing lmfao" , 
            "author" : "affan" , 
            "email" : "fareed320@gmail.com" , 
            "phone" : "6309232300" , 
            "img_uri" : workouts_JSON[key][x][1] , 
            "category" : key , 
        }
        myobj['id'] = x
        r = requests.post(url, data = myobj)
        print(r.text)



# GET METHOD
r = requests.get(url)
print(r.text)















# MANUALLY PUT  / DELETE

# import requests


# url = 'http://127.0.0.1:8000/api/37'
# myobj = {
#     "id" : 3,
#     "title" : "python rest test",
#     "author" : "affan_changed.py",
#     "email" : "laflametoast@NOSHIT.com",
# }


# # POST
# r = requests.put(url, data = myobj)
# print(r)


# # DELETE
# r = requests.delete(url, data = myobj)
# print(r)



"""






# MANUALLY POSTING WORKOUTS
import requests
import json


url = 'http://127.0.0.1:8000/api/'

f = open("workouts.json" , "r")
workouts_JSON = json.loads( f.read() )
f.close()


for key in workouts_JSON:
    for x in range( 0 , len(workouts_JSON[key]) , 1):
        myobj = {
            "title" : workouts_JSON[key][x][0] , 
            "img_uri" : workouts_JSON[key][x][1] , 
            "description" : workouts_JSON[key][x][2] , 
            "category" : key , 
            "author" : "Admin" , 
            "email" : "admin@oyama.com" , 
            "phone" : "555555555" , 
        }
        myobj['id'] = x
        r = requests.post(url, data = myobj)
        print(r.text)