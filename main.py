from create_draft import create_gmail_draft
from send_message import send_gmail_message

def main():
  print("Welcome to terminal gmail...\n ")
  while(True):
    print("1. Create a draft.")
    print("2. Send a mail.")
    print("3. Quit.")
    choice = int(input("Enter your choice: "))
    print()

    if (choice == 1):
      to = input('Enter the email address of the recepient:\n\t')
      subject = input('Enter the title of the email:\n\t')
      body = input('Enter the draft message you want to send:\n\t')
      attachments = input('Enter the name of attachment files (single space(\' \') separated):\n\t')
      create_gmail_draft(to, subject, body, attachments)
    elif (choice == 2):
      to = input('Enter the email address of the recepient:\n\t')
      subject = input('Enter the title of the email:\n\t')
      body = input('Enter the draft message you want to send:\n\t')
      attachments = input('Enter the name of attachment files (single space(\' \') separated):\n\t')
      send_gmail_message(to, subject, body, attachments)
    else:
      print("Exiting the app...")
      break

    print()

if __name__ == "__main__":
  main()