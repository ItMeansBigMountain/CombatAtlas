from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.shortcuts import redirect
import os
import random
import string
import hashlib
import base64
import requests





def generate_code_verifier():
    token = os.urandom(40)
    return base64.urlsafe_b64encode(token).rstrip(b'=').decode('utf-8')

def generate_code_challenge(code_verifier):
    verifier_bytes = code_verifier.encode('utf-8')
    digest = hashlib.sha256(verifier_bytes).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('utf-8')

def generate_state():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(30))

def construct_authorize_url(client_id, redirect_uri, scope, state, code_challenge, client_secret):
    base_url = "https://twitter.com/i/oauth2/authorize"
    url = f"{base_url}?response_type=code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&scope={scope}&state={state}&code_challenge={code_challenge}&code_challenge_method=S256"
    return url

def get_access_token(code, client_id, redirect_uri, code_verifier, client_secret):
    url = "https://api.twitter.com/2/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier
    }
    if client_secret:
        auth_str = f"{client_id}:{client_secret}"
        auth_str_b64 = base64.b64encode(auth_str.encode()).decode()
        headers['Authorization'] = f"Basic {auth_str_b64}"
    response = requests.post(url, headers=headers, data=data)
    return response.json()




def get_user_info(access_token):
    url = "https://api.twitter.com/2/users/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=headers)
    return response.json()












def home(request):
    request.session.flush()
    return render(request, 'home.html')



def twitter_login(request):
    client_id = "cjZVMWhtQmNpTzRNLURUSTVqMDc6MTpjaQ"
    client_secret = "JlyMncKfmubtVt0u2hfc4IYHOyQWC0fXRgpLqRoUVueOIo_SRK"
    base_url = "http://127.0.0.1:8000/"
    redirect_uri = base_url + "twitter_callback"
    scope = 'tweet.write%20tweet.read%20users.read%20follows.read%20follows.write'
    state = generate_state()
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    request.session['code_verifier'] = code_verifier

    url = construct_authorize_url(client_id, redirect_uri, scope, state, code_challenge, client_secret)
    return redirect(url)

def twitter_callback(request):
    client_id = "cjZVMWhtQmNpTzRNLURUSTVqMDc6MTpjaQ"
    client_secret = "JlyMncKfmubtVt0u2hfc4IYHOyQWC0fXRgpLqRoUVueOIo_SRK"
    base_url = "http://127.0.0.1:8000/"
    redirect_uri = base_url + "twitter_callback"
    
    code = request.GET.get('code')
    
    code_verifier = request.session.get('code_verifier')

    token_response = get_access_token(code, client_id, redirect_uri, code_verifier, client_secret)

    request.session['access_token'] = token_response.get("access_token")

    return redirect(dashboard)



def dashboard(request):
    access_token = request.session.get('access_token')
    user_info = get_user_info(access_token)
    return render(request,'dashboard.html', context={"user_info":user_info})







@csrf_exempt
def post_tweet(request):
    if request.method == 'POST':
        access_token = request.session.get('access_token')
        tweet_content = request.POST.get('tweet')

        url = "https://api.twitter.com/2/tweets"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "text": tweet_content
        }
        response = requests.post(url, headers=headers, json=data)

        return JsonResponse(response.json())
    else:
        return JsonResponse({"error": "This view only accepts POST requests."})
