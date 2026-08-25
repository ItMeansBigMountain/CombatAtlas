from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('twitter_login/', views.twitter_login, name='twitter_login'),
    path('twitter_callback/', views.twitter_callback, name='twitter_callback'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('post_tweet/', views.post_tweet, name='post_tweet')

]