import base64
import os
import mimetypes
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
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

def create_gmail_draft(to, subject, body, *attachments):
    creds = get_creds()

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()
        message.set_content(body)
        message['To'] = to
        message['From'] = 'mridulmaikhuri1234@gmail.com'
        message['Subject'] = subject

        # Adding attachments to mail
        for attachment in attachments:
            print(attachment, type(attachment))
            attachment_filename = attachment
            type_subtype, _ = mimetypes.guess_type(attachment_filename) # guessing the MIME type
            maintype, subtype = type_subtype.split("/")
            with open(attachment_filename, "rb") as fp:
                attachment_data = fp.read()
            message.add_attachment(attachment_data, maintype, subtype, filename=attachment_filename)

        #encode message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'message': {'raw': encoded_message}}

        draft = (
            service.users()
            .drafts()
            .create(userId='me', body=create_message)
            .execute()
        )

        print(f'Draft with draft id  {draft['id']} is successfully created.')
    except HttpError as e:
        print(f'An error occured: {e}')
        draft = None
    return draft

if __name__ == '__main__':
    to = input('Enter the email address of the recepient:\n\t')
    subject = input('Enter the title of the email:\n\t')
    body = input('Enter the draft message you want to send:\n\t')
    attachments = input('Enter the path of attachment files (single space(\' \') separated):\n\t')
    create_gmail_draft(to, subject, body, attachments)