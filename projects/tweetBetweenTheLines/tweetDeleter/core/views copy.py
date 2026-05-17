import requests
from django.shortcuts import redirect, render
from django.http import HttpResponse
from urllib.parse import urlparse, parse_qs , urlencode
import os
import base64
import hashlib
import string
import random

# Twitter API credentials
client_id = "cjZVMWhtQmNpTzRNLURUSTVqMDc6MTpjaQ"
client_secret = "JlyMncKfmubtVt0u2hfc4IYHOyQWC0fXRgpLqRoUVueOIo_SRK"
base_url = "http://127.0.0.1:8000/"
redirect_uri = base_url + "twitter_callback"
scopes = "tweet.read,tweet.write,tweet.moderate.write,users.read,follows.read,follows.write,offline.access,space.read,mute.read,mute.write,like.read,like.write,list.read,list.write,block.read,block.write,bookmark.read,bookmark.write".split(',')

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

def home(request):
    request.session.flush()
    return render(request, 'home.html')

def twitter_login(request):
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    state = generate_state()

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state
    }

    request.session['redirect_url'] = "https://twitter.com/i/oauth2/authorize?" + urlencode(params)
    request.session['code_verifier'] = code_verifier
    request.session['state'] = state
    return redirect(request.session['redirect_url'])

def twitter_callback(request):
    original_redirect_uri = request.session['redirect_url']
    original_code_verifier = request.session['code_verifier']
    original_state = request.session['state']

    full_url = request.build_absolute_uri()
    parsed_url = urlparse(full_url)
    params = parse_qs(parsed_url.query)
    returned_code = params.get('code', [None])[0]
    returned_state = params.get('state', [None])[0]

    if not returned_code:
        return HttpResponse("Invalid state parameter", status=400)


    if not returned_state or original_state != returned_state:
        return HttpResponse("Invalid state parameter", status=400)

    token_data = {
        "grant_type": "authorization_code",
        "code": returned_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "code_verifier": original_code_verifier,
        "client_secret": client_secret,
    }

    # client_id and client_secret are your API key and API secret key respectively
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')
    headers = {"Authorization": f"Basic {credentials}"}
    response = requests.post("https://api.twitter.com/oauth2/token", data=token_data, headers=headers)

    
    if response.status_code == 200:
        json_response = response.json()
        access_token = json_response.get("access_token")
        request.session['access_token'] = access_token
    else:
        print(f"Failed to get access token: {response.content}")
    return redirect('dashboard')

def dashboard(request):
    access_token = request.session.get('access_token')
    # Add your code to interact with the Twitter API using the access token
    return render(request, 'dashboard.html')
