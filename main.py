import base64
from dotenv import dotenv_values
import requests
import json

config = dotenv_values('.env')
CLIENT_ID = config.get('CLIENT_ID')
CLIENT_SECRET = config.get('CLIENT_SECRET') 
REDIRECT_URI = config.get('REDIRECT_URI')

# Authorize user account
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
    refreshToken.access_token = r.json()['access_token']
refreshToken()

# Creates a Tweet from authenticated user
def postTweet(message):
    post_tweet_url = 'https://api.twitter.com/2/tweets'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {refreshToken.access_token}'
    }
    message = {
        'text': message
    }
    r = requests.post(post_tweet_url, headers=headers, data=json.dumps(message))
    print(r.json())
message = input('Whats on your mind?:\n') # Send your tweet
postTweet(message)    

# get user by username 
def getUser(username):
    req_user_url = 'https://api.twitter.com/2/users/by'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {refreshToken.access_token}'
    }
    username = {
        'usernames': username
    }
    r = requests.get(req_user_url, headers=headers, params=username)
    data = r.text
    parsed_data = json.loads(data)
    print(r.json())
    
    # loop response for user id
    for user in parsed_data['data']:
        getUser.user_id = user['id']
        print(getUser.user_id)
username = input('Enter a username:\n')
getUser(username)