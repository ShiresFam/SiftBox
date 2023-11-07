import json
import os
from O365 import Account

# from app.utils.o365_token import token_backend

# credentials = (os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))

# account = Account(credentials, token_backend=token_backend)

# mailbox = account.mailbox()

# inbox = mailbox.inbox_folder()
# for message in inbox.get_messages():
#     print(message)


def get_user_emails(account: Account):
    mailbox = account.mailbox()
    inbox = mailbox.inbox_folder()
    messages = inbox.get_messages(query="isRead eq false")
    emails = []
    count = 0
    for message in messages:
        email = {
            "id": message.object_id,
            "to": [recipient.address for recipient in message.to],
            "cc": [recipient.address for recipient in message.cc],
            "bcc": [recipient.address for recipient in message.bcc],
            "created": message.created.isoformat(),
            "attachments": [attachment.name for attachment in message.attachments],
            "importance": str(message.importance.value),
            "subject": message.subject,
            "sender": message.sender.address if message.sender else None,
            "content": message.get_body_text(),
        }
        count += 1
        emails.append(email)
    return {"unread_count": count, "emails": emails}


def reply_to_email(account: Account, email_id: str, reply_text: str):
    mailbox = account.mailbox()
    message = mailbox.get_message(email_id)
    if message:
        message.reply(body=reply_text)
    else:
        print(f"No email found with id {email_id}")


def logout(account: Account):
    if account.is_authenticated:
        account.con.token_backend.delete_token()


def mark_as_read(account: Account, email_id: str):
    mailbox = account.mailbox()
    message = mailbox.get_message(email_id)
    if message:
        read = message.mark_as_read()
        print(read)
    else:
        print(f"No email found with id {email_id}")
