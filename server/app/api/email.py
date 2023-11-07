import json
import os
from fastapi import Request, Response, HTTPException, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from O365 import Account
from typing import List, Optional

from pydantic import BaseModel
from app.utils.o365_token import token_backend
from app.core.email.outlook_email import get_user_emails
from app.schemas.email import (
    Email,
    EmailMetadata,
    EmailPriority,
    EmailSummary,
    EmailImportant,
    TodoList,
    Todo,
)
from app.core.llm.chatgpt import (
    create_todo_list,
    send_email_metadata,
    summarize_emails,
)
from datetime import datetime

router = APIRouter(prefix="/auth")
mail_router = APIRouter(prefix="/mail")
credentials = (os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
isDev = os.getenv("DEV")
print(isDev)
web_url = (
    "https://localhost:8000/auth/stepone"
    if isDev == "1"
    else "https://localhost:8443/api/auth/stepone"
)
print(web_url)
print(f"credentials: {credentials}")
my_scopes = ["https://graph.microsoft.com/.default", "offline_access"]


class EmailResponse(BaseModel):
    unread_count: int
    emails: List[Email]


@router.get("/stepone")
async def auth_step_one():
    # callback = absolute url to auth_step_two_callback() page, https://domain.tld/steptwo
    callback = "https://localhost:8000/auth/steptwo"  # Example

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
    callback = "https://localhost:8000/auth/steptwo"  # Example
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
        return RedirectResponse(url="https://localhost:8443")

    raise HTTPException(status_code=400, detail="Authentication failed")


@router.get("/me")
async def get_user(request: Request):
    account = Account(credentials, token_backend=token_backend)
    if account.is_authenticated:
        return account.get_current_user().display_name
    else:
        return JSONResponse(
            {"redirect": True, "url": web_url},
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
        email_data = get_user_emails(account)
        emails = [Email(**email) for email in email_data["emails"]]

        return EmailResponse(unread_count=email_data["unread_count"], emails=emails)


@mail_router.get("/metadata")
async def check_metadata(request: Request):
    account = Account(credentials, token_backend=token_backend)
    if account.is_authenticated:
        email_data = get_user_emails(account)
        email_metadata = [EmailMetadata(**email) for email in email_data["emails"]]
        emails = [Email(**email) for email in email_data["emails"]]
        important_response = await send_email_metadata(emails)
        print(f"Imporant response: {important_response}")
        print(f"length of important response: {len(important_response)}")
        important_ids = [email.id for email in important_response if email.is_important]
        print(f"Imporant ids: {important_ids}")
        print(f"length of important ids: {len(important_ids)}")
        important_emails = [email for email in emails if email.id in important_ids]
        print(f"length of important emails: {len(important_emails)}")
        summaries: list[EmailSummary] = await summarize_emails(important_emails)
        print(f"length of summaries: {len(summaries)}")
        todo_emails = [
            Email(
                **{
                    **email.dict(),
                    "created": email.created.isoformat()
                    if isinstance(email.created, datetime)
                    else email.created,
                    "priority_rating": next(
                        (
                            e.priority_rating
                            for e in important_response
                            if e.id == email.id
                        ),
                        None,
                    ),
                    "summary": next(
                        (s.summary for s in summaries if s.id == email.id),
                        None,
                    ),
                }
            )
            for email in emails
            if email.id in important_ids
        ]

        todo_list = await create_todo_list(todo_emails)

        print(f"Todolist: {todo_list}")
        return todo_list
