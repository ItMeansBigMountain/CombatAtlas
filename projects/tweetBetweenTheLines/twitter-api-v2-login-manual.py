import requests
import base64
import webbrowser


import requests
from django.shortcuts import redirect, render
from django.http import HttpResponse
from urllib.parse import urlparse, parse_qs , urlencode
import os
import base64
import hashlib
import string
import random


# Step 1: Construct an Authorize URL
def construct_authorize_url(client_id, redirect_uri, scope, state, code_challenge):
    base_url = "https://twitter.com/i/oauth2/authorize"
    url = f"{base_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state={state}&code_challenge={code_challenge}&code_challenge_method=plain"
    return url

# Step 3: POST oauth2/token - Access Token
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

# Step 5: POST oauth2/token - refresh token
def refresh_token(refresh_token, client_id, client_secret=None):
    url = "https://api.twitter.com/2/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': client_id
    }
    if client_secret:
        auth_str = f"{client_id}:{client_secret}"
        auth_str_b64 = base64.b64encode(auth_str.encode()).decode()
        headers['Authorization'] = f"Basic {auth_str_b64}"
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Step 6: POST oauth2/revoke - Revoke Token
def revoke_token(token, client_id, client_secret=None):
    url = "https://api.twitter.com/2/oauth2/revoke"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'token': token,
        'client_id': client_id
    }
    if client_secret:
        auth_str = f"{client_id}:{client_secret}"
        auth_str_b64 = base64.b64encode(auth_str.encode()).decode()
        headers['Authorization'] = f"Basic {auth_str_b64}"
    response = requests.post(url, headers=headers, data=data)
    return response.json()



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





def main():
    client_id = "cjZVMWhtQmNpTzRNLURUSTVqMDc6MTpjaQ"
    client_secret = "JlyMncKfmubtVt0u2hfc4IYHOyQWC0fXRgpLqRoUVueOIo_SRK"
    base_url = "http://127.0.0.1:8000/"
    redirect_uri = base_url + "twitter_callback"
    scope = 'tweet.read%20users.read%20follows.read%20follows.write'
    state = generate_state()
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    
    # Step 1: Construct an Authorize URL
    url = construct_authorize_url(client_id, redirect_uri, scope, state, code_challenge)
    
    # Open the URL in a web browser
    webbrowser.open(url)

    # The user will be redirected to the redirect_uri after authorizing the app
    # You need to extract the 'code' parameter from the redirected URL
    # Then you can use this 'code' to get an access token
    code = input('extracted_code_from_redirected_url')
    token_response = get_access_token(code, client_id, redirect_uri, code_challenge , client_secret)

    print(token_response)

if __name__ == "__main__":
    main()
