import base64
import os

from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

def get_creds():
    creds = None
    if os.path.exists("credentials/compose_token.json"):
        creds = Credentials.from_authorized_user_file("credentials/compose_token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("credentials/compose_token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def send_gmail_message(to, subject, body):
  creds = get_creds()

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content(body)

    message["To"] = to
    message["From"] = 'mridulmaikhuri1234@gmail.com'
    message["Subject"] = subject

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message with message id: {send_message["id"]} sent.')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


if __name__ == "__main__":
    to = input('Enter the email address of the recepient:\n\t')
    subject = input('Enter the title of the email:\n\t')
    body = input('Enter the draft message you want to send:\n\t')
    send_gmail_message(to, subject, body)