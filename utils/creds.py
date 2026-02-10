import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

COMPOSE_TOKEN_PATH = "credentials/compose_token.json"
CREDENTIALS_PATH = "credentials/credentials.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

def get_compose_creds():
    creds = None
    if os.path.exists(COMPOSE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(COMPOSE_TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(COMPOSE_TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds