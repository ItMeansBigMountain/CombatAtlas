# django
from django.shortcuts import render
from django.http  import JsonResponse
from django.core.files.base import ContentFile, File

# files
from .models import Workout , CATEGORY_CHOICES
from .serializers import WorkoutSerializer

# rest framework
from rest_framework.parsers import JSONParser , MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.views import APIView


# extra functionality
import random
CATEGORY_CHOICES = [ x[0] for x in CATEGORY_CHOICES  ]
import urllib






# # ROUTE: "api/"
@api_view(['GET', 'POST'])
def Workout_list(request):
    # FETCH DATA BASE
    if request.method == "GET":
        Workouts = Workout.objects.all()
        serializer = WorkoutSerializer(Workouts , many=True)
        return Response( serializer.data  )
    
    # RECIEVES JSON POST IN request.data
    elif request.method == "POST":
        filtered_workouts = Workout.objects.filter(title=request.data['title'] , category=request.data['category'])
        if len(filtered_workouts) > 0:
            return Response({"res":"Exercise Already In The System!"} , status=status.HTTP_401_UNAUTHORIZED)



        # CONVERT URI STRING INTO IMAGE FILE
        data_uri = request.data['img_uri']
        file_extention = data_uri.split("/")[1].split(";")[0]
        
        # creating image file..
        if len(file_extention):
            with urllib.request.urlopen(data_uri) as response:
                data = response.read()
            with open(f"media/{request.data['title']}.{file_extention}", "wb") as f:
                f.write(data)


        serializer =  WorkoutSerializer(data=request.data) 

        # VALIDATE
        if serializer.is_valid():
            serializer.save()
            r =  dict(request.data)
            r['res'] =  "Submitted!"
            return Response( r , status=status.HTTP_201_CREATED )
        else:
            print(serializer.errors)
            return Response({"res":"Submition Data Issue"} , status=status.HTTP_401_UNAUTHORIZED)





# ROUTE: "api/workout-keys"
@api_view(['GET'])
def fetch_categories(request):
    # FETCH DATA BASE
    if request.method == "GET":
        return Response( CATEGORY_CHOICES  )
    


# ROUTE: "api/workout/<str:group>/<str:community>"
@api_view(['GET'])
def Workout_detail(request , group , community):
    # Fetch workouts from db
    try:
        # WORKOUT SEARCH PARAM
        if len(group.split("-")) > 1:
            group = group.lower()
        else:
            group = group.capitalize()

        # COMMUNITY BOOLEAN
        community = community.lower()
        if community.startswith("t"):
            community = True
        else:
            community = False
        Workouts = Workout.objects.filter(category=group , community_contrib=community)
    except Workouts.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response( str(e) ,status=status.HTTP_404_NOT_FOUND)
    
    
    # RETURNS RANDOM WORKOUT WITH SPECIFIED MUSCLE GROUP
    if request.method == "GET":
        if not len(Workouts):
            return Response("No Workouts Found Using Parameters" , status=status.HTTP_400_BAD_REQUEST)

        random_number = random.randint(0, len(Workouts) - 1 )
        serializer = WorkoutSerializer( Workouts[random_number] )
        return Response(serializer.data , status=status.HTTP_200_OK)



# ROUTE: "api/workout/<str:group>/<int:pk>"
@api_view(['GET'])
def specific_workout(request , group , pk):
    # Fetch workouts from db
    try:
        # WORKOUT SEARCH PARAM
        if len(group.split("-")) > 1:
            group = group.lower()
        else:
            group = group.capitalize()

        workout = Workout.objects.get(category=group , pk=pk)
    except Exception as e:
        return Response( str(e) ,status=status.HTTP_404_NOT_FOUND)
    
    
    # RETURNS RANDOM WORKOUT WITH SPECIFIED MUSCLE GROUP
    if request.method == "GET":
        serializer = WorkoutSerializer( workout )
        return Response(serializer.data , status=status.HTTP_200_OK)



