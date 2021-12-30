import base64
from dotenv import dotenv_values
import requests

config = dotenv_values('.env')
CLIENT_ID = config.get('CLIENT_ID')
CLIENT_SECRET = config.get('CLIENT_SECRET') 
REDIRECT_URI = config.get('REDIRECT_URI')

def authUrl():
    auth_url = 'https://twitter.com/i/oauth2/authorize'
    scopes = ['tweet.write', 'tweet.read', 'users.read', 'offline.access']
    state = 'state'
    param = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(scopes),
        'state': state,
        'code_challenge': 'challenge',
        'code_challenge_method': 'plain'
    }
    r = requests.get(auth_url, params=param)
    
    if r.status_code != 200:
        print(f'Error: {r.status_code}')
        return r.close()
    
    print(r.url)

def reqToken(code):
    token_url = 'https://api.twitter.com/2/oauth2/token'  
    rawAuth = f'{CLIENT_ID}:{CLIENT_SECRET}'
    auth = base64.b64encode(rawAuth.encode('ascii')).decode('ascii')
    header = { 
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth}'
    }
    data = {
        'code': code, 
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': 'challenge'
    }
    r = requests.post(token_url, headers=header, params=data)
    if r.status_code != 200:
        print(f'Error: {r.status_code}')

    reqToken.refresh_token = r.json()['refresh_token']     

authUrl()
code = input('enter code from url after authenticating: ') # auth code from url
reqToken(code)

# refresh token allows app to obtain new access token w/o user prompt 
def refreshToken():
    refresh_url = 'https://api.twitter.com/2/oauth2/token'
    headers = {
        'Content-Type': 'authorization/x-www-form-urlencoded'
    }
    data = {
        'refresh_token': reqToken.refresh_token,
        'grant_type': 'refresh_token',
        'client_id': CLIENT_ID
    }
    r = requests.post(refresh_url, headers=headers, params=data)
    print(r.json()['access_token']) 
refreshToken()