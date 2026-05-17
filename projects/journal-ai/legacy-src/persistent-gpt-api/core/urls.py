from django.urls import path, include
from . import views
from django.http import HttpResponse



urlpatterns = [
    # Root URL configuration
    path("", lambda r : HttpResponse("Welcome to the Chat GPT persistent data API!"), name='home'),

    # REST Framework auth URLs
    path('api-auth/', include('rest_framework.urls')),

    # Social Auth URLs
    path('auth/', include('social_django.urls', namespace='social')),
    path('display-token/', views.display_token, name='display-token'),

    # Custom user related URLs
    # path('users/', views.custom_user_list, name='user-list'),
    path('users/<int:pk>/', views.custom_user_detail, name='user-detail'),

    # Chat session related URLs
    path('chats/', views.chat_session_list, name='chat-session-list'),
    path('chats/<uuid:session_id>/', views.chat_session_detail, name='chat-session-detail'),

    # Chat message related URLs
    path('chats/<uuid:session_id>/messages/', views.create_chat_message, name='create-chat-message'),  
    path('chats/<uuid:session_id>/get_messages/', views.get_chat_messages, name='get-chat-messages'),

    # Privacy Policy URL
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
]


# NGROK OAUTH GOOGLE LOGIN 
# https://reasonably-fit-impala.ngrok-free.app/auth/login/google-oauth2/
