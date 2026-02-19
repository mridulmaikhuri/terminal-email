import base64
import mimetypes

from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.creds import get_compose_creds
from utils.email_validator import is_email_valid

def send_gmail_message(to, subject, body, *attachments):
  if (not is_email_valid(to)):
      print("E-mail address of recepient is not valid")
      return
  
  creds = get_compose_creds()

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content(body)

    message["To"] = to
    message["From"] = 'mridulmaikhuri1234@gmail.com'
    message["Subject"] = subject

    # Adding attachments to mail
    for attachment in attachments:
        print(attachment, type(attachment))
        attachment_filename = attachment
        type_subtype, _ = mimetypes.guess_type(attachment_filename)
        maintype, subtype = type_subtype.split("/")
        with open(attachment_filename, "rb") as fp:
            attachment_data = fp.read()
        message.add_attachment(attachment_data, maintype, subtype, filename=attachment_filename)

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message with message id: {send_message["id"]} successfully sent.')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


if __name__ == "__main__":
    to = input('Enter the email address of the recepient:\n\t')
    subject = input('Enter the title of the email:\n\t')
    body = input('Enter the draft message you want to send:\n\t')
    attachments = input('Enter the path of attachment files (single space(\' \') separated):\n\t').split()
    send_gmail_message(to, subject, body, *attachments)