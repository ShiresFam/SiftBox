import json
import os
from fastapi import Request, Response, HTTPException, APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from O365 import Account
from typing import List, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.models import get_db
from app.utils.o365_token import token_backend
from app.core.email.outlook_email import (
    get_user_emails,
    mark_as_read,
    reply_to_email,
    logout,
)
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
    suggestResponse,
    summarize_emails,
    summarize_single_email,
)
import app.db.crud as crud
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


@router.get("/logout")
async def logout_0365(request: Request):
    account = Account(credentials, token_backend=token_backend)
    logout(account)
    return JSONResponse({"message": "Logged out successfully"}, status_code=200)


@mail_router.post("/reply/{email_id}")
async def reply(request: Request, email_id: str = None):
    print(email_id)
    account = Account(credentials, token_backend=token_backend)
    if account.is_authenticated:
        reply_text = await request.body()
        reply_to_email(account, email_id, reply_text)
        return JSONResponse({"message": "Reply sent successfully"}, status_code=200)
    else:
        return JSONResponse(
            {"message": "Not logged in"},
            status_code=401,
        )


@mail_router.get("/mark-as-read/{email_id}")
async def mark_read(
    request: Request, db: Session = Depends(get_db), email_id: str = None
):
    account = Account(credentials, token_backend=token_backend)
    if account.is_authenticated:
        mark_as_read(account, email_id)
        crud.delete_email_by_id(db, email_id)
        return JSONResponse({"message": "Email marked as read"}, status_code=200)
    else:
        return JSONResponse(
            {"message": "Not logged in"},
            status_code=401,
        )


@mail_router.get("/unread")
async def get_unread(request: Request, db: Session = Depends(get_db)):
    account = Account(credentials, token_backend=token_backend)
    if account.is_authenticated:
        email_data = get_user_emails(account)
        emails = [Email(**email) for email in email_data["emails"]]
        crud.create_emails(db, emails)

        return EmailResponse(unread_count=email_data["unread_count"], emails=emails)

    else:
        account.con.refresh_token()
        email_data = get_user_emails(account)
        emails = [Email(**email) for email in email_data["emails"]]
        crud.create_emails(db, emails)

        return EmailResponse(unread_count=email_data["unread_count"], emails=emails)


@mail_router.get("/create-important")
async def get_email_db(request: Request, db: Session = Depends(get_db)):
    emails = crud.get_emails(db)
    important_response = await send_email_metadata(emails)
    print(important_response)
    crud.create_email_important_bulk(db, important_response)
    crud.update_priority_ratings(db, important_response)
    all_important = crud.get_email_important_bulk(db)
    return all_important


@mail_router.get("/get-important")
async def get_important_emails(request: Request, db: Session = Depends(get_db)):
    important_emails = crud.get_email_important_bulk(db)
    return important_emails


@mail_router.get("/get-important/emails")
async def get_important_emails(request: Request, db: Session = Depends(get_db)):
    important_emails = crud.get_important_emails(db)
    return important_emails


@mail_router.get("/create-summaries")
async def create_summaries(request: Request, db: Session = Depends(get_db)):
    important_emails = crud.get_important_emails(db)
    summaries: list[EmailSummary] = await summarize_emails(important_emails)
    crud.update_email_summaries(db, summaries)
    return summaries


@mail_router.get("/create-summary/{email_id}")
async def create_summary(
    request: Request, db: Session = Depends(get_db), email_id: str = None
):
    email = crud.get_email(db, email_id)
    summary: EmailSummary = await summarize_single_email(email)
    crud.update_email_summary(db, summary)
    updated_email = crud.get_email(db, email_id)
    return updated_email


@mail_router.get("/create-todolist")
async def create_todolist(request: Request, db: Session = Depends(get_db)):
    important_emails = crud.get_important_emails(db)
    crud.delete_all_todos(db)
    todo_list: TodoList = await create_todo_list(important_emails)
    created_list = crud.create_todos_bulk(db, todo_list.todo)
    return created_list


@mail_router.get("/todolist")
async def get_todolist(request: Request, db: Session = Depends(get_db)):
    todo_list = crud.get_todos(db)
    return todo_list


@mail_router.get("/response/{email_id}")
async def get_response(
    request: Request, db: Session = Depends(get_db), email_id: str = None
):
    email = crud.get_email(db, email_id)
    response = await suggestResponse(email)
    return response


@mail_router.put("/todo-complete/{todo_id}")
async def complete_todo(
    request: Request, db: Session = Depends(get_db), todo_id: int = None
):
    crud.set_todo_completed(db, todo_id)
    return JSONResponse(
        status_code=200, content={"message": "Todo marked as completed"}
    )


@mail_router.put("/todo-delete/{todo_id}")
async def delete_todo(
    request: Request, db: Session = Depends(get_db), todo_id: int = None
):
    crud.set_todo_deleted(db, todo_id)
    return JSONResponse(status_code=200, content={"message": "Todo marked as deleted"})
