from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from social_django.utils import load_strategy, load_backend
from social_core.actions import do_complete
from social_core.exceptions import AuthException

from django.shortcuts import redirect, render
from django.http import JsonResponse

from .models import CustomUser, ChatSession, ChatMessage
from .serializers import CustomUserSerializer, ChatSessionSerializer, ChatMessageSerializer

from datetime import datetime
import json


def health_check(request):
    return JsonResponse({"status": "ok", "service": "journal-ai-api"})


# Custom User Views
# @api_view(['GET', 'POST'])
# @permission_classes([permissions.IsAuthenticated])
# def custom_user_list(request):
#     if request.method == 'GET':
#         users = CustomUser.objects.all()
#         serializer = CustomUserSerializer(users, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def custom_user_detail(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# Chat Session Views
@api_view(['GET', 'POST'])
def chat_session_list(request):
    unique_identifier = request.GET.get('unique_identifier', None)

    if request.method == 'GET':
        if unique_identifier:
            try:
                q_user = CustomUser.objects.get(unique_identifier=unique_identifier)
                sessions = ChatSession.objects.filter(user=q_user)
                # active_sessions = [session for session in sessions if session.session_data.get('status') == 'active']
            except CustomUser.DoesNotExist:
                return Response({"error": "User with this unique identifier does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Handle case when unique_identifier is not provided in the request
            return Response({"error": "Unique identifier is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if unique_identifier:
            try:
                q_user = CustomUser.objects.get(unique_identifier=unique_identifier)
            except CustomUser.DoesNotExist:
                return Response({"error": "User with this unique identifier does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # Check if there's an active session for the user and continue it
            active_session = ChatSession.objects.filter(user=q_user, session_data__contains={'status': 'active'}).first()
            if active_session:
                serializer = ChatSessionSerializer(active_session)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # If no active session, create a new one
            new_session = {"messages": [], "status": "active"}
            serializer = ChatSessionSerializer(data={'user': q_user.id, 'session_data': new_session})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            # Handle case when unique_identifier is not provided in the request for POST method
            return Response({"error": "Unique identifier is required for creating a chat session"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([permissions.IsAuthenticated])
def chat_session_detail(request, session_id):
    unique_identifier = request.GET.get('unique_identifier', None)

    if not unique_identifier:
        return Response({"error": "Unique identifier is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        q_user = CustomUser.objects.get(unique_identifier=unique_identifier)
    except CustomUser.DoesNotExist:
        return Response({"error": "User with this unique identifier does not exist"}, status=status.HTTP_404_NOT_FOUND)

    try:
        session = ChatSession.objects.get(session_id=session_id, user=q_user)
    except ChatSession.DoesNotExist:
        return Response({"error": "Chat session not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)

    elif request.method == 'PUT':
        current_session_data = json.loads(session.session_data)
        updated_data = request.data.get('session_data')

        if updated_data and 'messages' in updated_data:
            current_session_data['messages'].extend(updated_data['messages'])
            session.session_data = json.dumps(current_session_data)
            session.save(update_fields=['session_data'])

            serializer = ChatSessionSerializer(session)
            return Response(serializer.data)
        return Response({"error": "Invalid session data"}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# New views for handling ChatMessages
@api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
def create_chat_message(request, session_id):
    unique_identifier = request.GET.get('unique_identifier', None)

    if not unique_identifier:
        return Response({"error": "Unique identifier is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        q_user = CustomUser.objects.get(unique_identifier=unique_identifier)
    except CustomUser.DoesNotExist:
        return Response({"error": "User with this unique identifier does not exist"}, status=status.HTTP_404_NOT_FOUND)

    try:
        session = ChatSession.objects.get(session_id=session_id, user=q_user)
    except ChatSession.DoesNotExist:
        return Response({"error": "Chat session not found"}, status=status.HTTP_404_NOT_FOUND)

    message_data = request.data.get('message')
    if message_data:
        new_message = {'text': message_data, 'timestamp': str(datetime.now())}
        current_session_data = json.loads(session.session_data)
        current_session_data.get('messages', []).append(new_message)
        session.session_data = json.dumps(current_session_data)
        session.save(update_fields=['session_data'])

        return Response({'message': 'Message added successfully'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Invalid message data'}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
def get_chat_messages(request, session_id):
    unique_identifier = request.GET.get('unique_identifier', None)

    if not unique_identifier:
        return Response({"error": "Unique identifier is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        q_user = CustomUser.objects.get(unique_identifier=unique_identifier)
    except CustomUser.DoesNotExist:
        return Response({"error": "User with this unique identifier does not exist"}, status=status.HTTP_404_NOT_FOUND)

    try:
        session = ChatSession.objects.get(session_id=session_id, user=q_user)
    except ChatSession.DoesNotExist:
        return Response({"error": "Chat session not found"}, status=status.HTTP_404_NOT_FOUND)

    session_data = json.loads(session.session_data)
    messages = session_data.get('messages', [])
    return Response({'messages': messages})







# OAUTH HANDLING
@permission_classes([permissions.IsAuthenticated])
def display_token(request):
    print(request.user)
    content = {
        'user':request.user,
        'token': request.user.unique_identifier
    }
    return render(request, 'display_token.html', content)







# PRIVACY POLICY
def privacy_policy(request):
    privacy_policy = {
        "Introduction": "This policy outlines data collection, usage, and rights related to our services. Use of our services constitutes agreement to this policy.",
        "Data Collection and Use": "We collect various information, including chat data and user-identifiable information, to provide and improve our service.",
        "Data Ownership and Rights": "All data collected is our property. We have the right to analyze, sell, change, or delete this data at our discretion.",
        "User Data Inquiries and Management": "Users may contact persistentgpt@gmail.com for data inquiries. Requests for data manipulation or access are subject to our discretion.",
        "Liability and Indemnification": "We are not liable for the use of collected data. Users indemnify us against all related claims and expenses.",
        "Amendments to the Privacy Policy": "We may modify this policy at any time. Continued use after modifications implies acceptance of these changes.",
        "Contact Us": "For questions about this policy, contact us at persistentgpt@gmail.com."
    }
    return JsonResponse(privacy_policy)


