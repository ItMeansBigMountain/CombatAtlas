from django.urls import path
from django.http import HttpResponse 
from . import views



urlpatterns = [
    path("" , lambda request : HttpResponse("welcome!") ),
    path("api/" , views.Workout_list ),
    path("api/workout-keys" , views.fetch_categories ),
    path("api/<str:group>/<str:community>" , views.Workout_detail ),
    path("api/<str:group>/<int:pk>" , views.specific_workout ),
]
