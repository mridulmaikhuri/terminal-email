from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.creds import get_read_creds

def list_messages():
    creds = get_read_creds()

    try:
        service = build("gmail", "v1", credentials=creds)
        results = (
            service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
        )
        messages = results.get("messages", [])

        if not messages:
            print("No messages found.")
            return

        print("Messages:")
        for i in range(50):
            message = messages[i]
            print(f'Message ID: {message["id"]}')
            msg = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
            )
            print(f'  Subject: {msg["snippet"]}')

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    list_messages()