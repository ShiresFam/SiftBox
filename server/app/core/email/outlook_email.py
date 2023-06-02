import os
from O365 import Account
from app.utils.o365_token import token_backend

credentials = (os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))

account = Account(credentials, token_backend=token_backend)

mailbox = account.mailbox()

inbox = mailbox.inbox_folder()
for message in inbox.get_messages():
    print(message)