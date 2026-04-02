"""
OAuth utilities for Django application
"""
import urllib.parse
import requests
import secrets


class SimpleOAuth2Client:
    def __init__(self, client_id, client_secret, auth_url, token_url, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.code = None
        self.token = None

    def get_authorization_url(self, state=None):
        """Generate the authorization URL for the user to visit"""
        if state is None:
            state = secrets.token_urlsafe(16)
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope,
            'response_type': 'code',
            'state': state,
            'access_type': 'offline'
        }
        
        return f"{self.auth_url}?{urllib.parse.urlencode(params)}", state

    def get_token(self, code=None):
        """Exchange authorization code for access token"""
        if code:
            self.code = code

        if not self.code:
            raise Exception("No authorization code provided")

        data = {
            'grant_type': 'authorization_code',
            'code': self.code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(self.token_url, data=data)

        if response.status_code != 200:
            raise Exception(f"Failed to get token: {response.text}")

        self.token = response.json()
        return self.token

    def refresh_token(self):
        """Refresh the access token using refresh token"""
        if not self.token or 'refresh_token' not in self.token:
            raise Exception("No refresh token available")

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.token['refresh_token'],
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(self.token_url, data=data)

        if response.status_code != 200:
            raise Exception(f"Failed to refresh token: {response.text}")

        self.token.update(response.json())
        return self.token

    def make_api_request(self, url, method='GET', headers=None, data=None):
        """Make an API request with the access token"""
        if not self.token:
            raise Exception("No access token available")

        if headers is None:
            headers = {}
        headers['Authorization'] = f"Bearer {self.token['access_token']}"

        response = requests.request(method, url, headers=headers, json=data)
        return response

    def get_user_info(self):
        """Get user info from Google OAuth"""
        response = self.make_api_request("https://www.googleapis.com/oauth2/v2/userinfo")
        return response.json()
