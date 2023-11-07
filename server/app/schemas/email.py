from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class EmailMetadata(BaseModel):
    id: str
    to: List[str]
    cc: Optional[List[str]]
    bcc: Optional[List[str]]
    created: datetime
    attachments: List[str]
    importance: Optional[str]
    subject: str
    sender: Optional[str]


class Email(EmailMetadata):
    content: str
    priority_rating: Optional[int] = None
    summary: Optional[str] = None


class EmailImportant(BaseModel):
    id: str
    is_important: bool
    is_spam: bool
    important_reason: Optional[str]
    spam_reason: Optional[str]
    priority_rating: Optional[int]


class EmailPriority(BaseModel):
    id: str
    priority_rating: int


class EmailSummary(BaseModel):
    id: str
    summary: str


class Todo(BaseModel):
    task: str
    priority: int


class TodoList(BaseModel):
    todo: List[Todo]
