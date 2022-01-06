# Connect to endpoints using OAuth 2.0 Authorization Code Flow with PKCE

Sample code flow for Twitter API v2 endpoints 
* [Twitter Documenation](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api)
* [OAuth 2.0 with PKCE](https://developer.twitter.com/en/docs/authentication/oauth-2-0/user-access-token)

## Getting started 
* [Create project/app in dashboard](https://developer.twitter.com/en/portal/dashboard)

### Python environment setup 
Python 3 required, built on 3.10.1

```bash
pip install requests
pip install python-dotenv
```
### Usage
Set up your environment variables. You can find credentials in your [Project & Apps developer portal](https://developer.twitter.com/en/portal/dashboard) 

```python
CLIENT_ID = {TWITTER_CLIENT_ID}
CLIENT_SECRET = {TWITTER_CLIENT_SECRET}
REDIRECT_URI = {TWITTER_REDIRECT_URI}
``` 

### Using .env 
* [Python-dotenv Documenation](https://pypi.org/project/python-dotenv/)

Add `.env` to root directory of your project
```
├── .env
└── main.py
```

```bash
TWITTER_CLIENT_ID=
TWITTER_CLIENT_SECRET=
TWITTER_REDIRECT_URI=
```
