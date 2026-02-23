from msal import ConfidentialClientApplication
import os
from dotenv import load_dotenv
import requests
from . import token_store

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

AUTHORITY = "https://login.microsoftonline.com/common"

SCOPES = [
    "User.Read",
    "Calendars.ReadWrite",
    "OnlineMeetings.ReadWrite"
]

REDIRECT_URI = "http://localhost:8000/auth/callback"

app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)

def get_auth_url():
    return app.get_authorization_request_url(
        SCOPES,
        redirect_uri=REDIRECT_URI
    )

def exchange_code_for_token(code):
    result = app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    if "access_token" in result:
        token_store.ACCESS_TOKEN = result["access_token"]
    return result

def get_user_profile(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers=headers
    )

    return response.json()