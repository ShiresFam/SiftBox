import os
from fastapi import Request, Response, HTTPException, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from O365 import Account
from typing import List, Optional

from pydantic import BaseModel
from app.utils.o365_token import token_backend
from app.core.email.outlook_email import get_user_emails

router = APIRouter(prefix="/auth")
mail_router = APIRouter(prefix="/mail")
credentials = (os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
my_scopes = ["https://graph.microsoft.com/.default", "offline_access"]


class Email(BaseModel):
    subject: str
    sender: str
    content: str


class EmailResponse(BaseModel):
    unread_count: int
    emails: List[Email]


@router.get("/stepone")
async def auth_step_one():
    # callback = absolute url to auth_step_two_callback() page, https://domain.tld/steptwo
    callback = "https://127.0.0.1:8000/auth/steptwo"  # Example

    account = Account(credentials, token_backend=token_backend)
    url, state = account.con.get_authorization_url(
        requested_scopes=my_scopes, redirect_uri=callback
    )

    # the state must be saved somewhere as it will be needed later
    global storedState
    storedState = state  # example...

    print(storedState)

    return RedirectResponse(url)


@router.get("/steptwo")
async def auth_step_two_callback(request: Request):
    params = request.query_params
    print(params)
    account = Account(credentials, token_backend=token_backend)

    # retrieve the state saved in auth_step_one
    my_saved_state = storedState  # example...

    # rebuild the redirect_uri used in auth_step_one
    callback = "https://127.0.0.1:8000/auth/steptwo"  # Example
    print("callback")
    print(callback)

    # get the request URL of the page which will include additional auth information
    # Example request: /steptwo?code=abc123&state=xyz456
    requested_url = f"{callback}?{params}"

    result = account.con.request_token(
        requested_url, state=my_saved_state, redirect_uri=callback
    )
    # if result is True, then authentication was successful
    # and the auth token is stored in the token backend
    if result:
        return RedirectResponse(url="https://127.0.0.1:3000")

    raise HTTPException(status_code=400, detail="Authentication failed")


@router.get("/me")
async def get_user(request: Request):
    account = Account(credentials, token_backend=token_backend)
    if account.is_authenticated:
        return account.get_current_user().display_name
    else:
        return JSONResponse(
            {"redirect": True, "url": "https://localhost:8000/auth/stepone"},
            status_code=307,
        )


@mail_router.get("/unread")
async def get_unread(request: Request):
    account = Account(credentials, token_backend=token_backend)
    if account.is_authenticated:
        email_data = get_user_emails(account)
        emails = [Email(**email) for email in email_data["emails"]]

        return EmailResponse(unread_count=email_data["unread_count"], emails=emails)

    else:
        account.con.refresh_token()
        data = get_user_emails(account)
