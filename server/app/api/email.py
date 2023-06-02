import os
from fastapi import Request, Response, HTTPException, APIRouter
from O365 import Account
from typing import Optional
from starlette.responses import RedirectResponse
from app.utils.o365_token import token_backend

router = APIRouter(prefix='/auth')
credentials = (os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))
my_scopes=['https://graph.microsoft.com/.default']

@router.get("/stepone")
async def auth_step_one():
    # callback = absolute url to auth_step_two_callback() page, https://domain.tld/steptwo
    callback = "http://localhost:8000/auth/steptwo"  # Example

    account = Account(credentials, token_backend=token_backend)
    url, state = account.con.get_authorization_url(requested_scopes=my_scopes,
                                                         redirect_uri=callback)

    # the state must be saved somewhere as it will be needed later
    global storedState
    storedState = state  # example...

    return RedirectResponse(url)


@router.get("/steptwo")
async def auth_step_two_callback(request: Request):
    params = request.query_params
    print(params)
    account = Account(credentials, token_backend=token_backend)

    # retrieve the state saved in auth_step_one
    my_saved_state = storedState  # example...

    # rebuild the redirect_uri used in auth_step_one
    callback = 'http://localhost:8000/auth/steptwo'  # Example
    print('callback')
    print(callback)


    # get the request URL of the page which will include additional auth information
    # Example request: /steptwo?code=abc123&state=xyz456
    requested_url = f"{callback}?{params}"

    result = account.con.request_token(requested_url,
                                             state=my_saved_state,
                                             redirect_uri=callback)
    # if result is True, then authentication was successful
    # and the auth token is stored in the token backend
    if result:
         mailbox = account.mailbox()
         inbox = mailbox.inbox_folder()
         for message in inbox.get_messages():
            print(message)
         return {"detail": "Authentication successful"}

    raise HTTPException(status_code=400, detail="Authentication failed")