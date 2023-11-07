import uuid
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.schemas.utils import to_camel


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
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )
    content: str
    priority_rating: Optional[int] = None
    summary: Optional[str] = None


class EmailImportant(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )
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


class EmailResponse(BaseModel):
    id: str
    response: str


class Todo(BaseModel):
    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, alias_generator=to_camel
    )
    id: Optional[str] = None
    task: str
    priority: int
    is_completed: Optional[bool] = False
    is_deleted: Optional[bool] = False


class TodoList(BaseModel):
    todo: List[Todo]
