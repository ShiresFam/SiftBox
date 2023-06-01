import os
import imaplib


def check_for_new_emails():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL('imap.example.com')

    # Authenticate with your email address and password
    mail.login('your_email@example.com', 'your_password')

    # Select the mailbox (e.g., Inbox)
    mail.select('INBOX')

    # Search for unread messages
    _, message_ids = mail.search(None, 'UNSEEN')

    # Process the new emails
    for message_id in message_ids[0].split():
        _, msg_data = mail.fetch(message_id, '(RFC822)')
        email_content = msg_data[0][1]
        # Process the email content as needed
        print("New email received!")
        print(email_content)

    # Close the mailbox connection
    mail.logout()