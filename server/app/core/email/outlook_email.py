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
