import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

CREDENTIALS_PATH = "credentials/credentials.json"

COMPOSE_TOKEN_PATH = "credentials/compose_token.json"
COMPOSE_SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

READ_TOKEN_PATH = "credentials/read_token.json"
READ_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_compose_creds():
    creds = None
    if os.path.exists(COMPOSE_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(COMPOSE_TOKEN_PATH, COMPOSE_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, COMPOSE_SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(COMPOSE_TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds

def get_read_creds():
    creds = None
    if os.path.exists(READ_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(READ_TOKEN_PATH, READ_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, READ_SCOPES)
            creds = flow.run_local_server(port=0)
        with open(READ_TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds