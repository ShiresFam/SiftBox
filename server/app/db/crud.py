from typing import List
from sqlalchemy import delete, update
from sqlalchemy.orm import Session
import uuid

from app.db.models import Email as EmailModel
from app.schemas.email import Email as EmailSchema, EmailSummary
from app.db.models import EmailImportant as EmailImportantModel
from app.schemas.email import EmailImportant as EmailImportantSchema
from app.schemas.email import Todo as TodoSchema
from app.schemas.email import TodoList
from app.db.models import Todo as TodoModel


def create_emails(db: Session, emails: List[EmailSchema]):
    db_emails = []
    for email in emails:
        db_email = db.query(EmailModel).filter(EmailModel.id == email.id).first()
        if db_email is None:
            db_email = EmailModel(**email.dict())
            db.add(db_email)
        db_emails.append(db_email)
    db.commit()
    return db_emails


def create_emails(db: Session, emails: List[EmailSchema]):
    db_emails = []
    for email in emails:
        db_email = db.query(EmailModel).filter(EmailModel.id == email.id).first()
        if db_email is None:
            db_email = EmailModel(**email.dict())
            db.add(db_email)
        db_emails.append(db_email)
    db.commit()
    return db_emails


def create_email_important(db: Session, email_important: EmailImportantSchema):
    db_email_important = EmailImportantModel(**email_important.dict())
    db.add(db_email_important)
    db.commit()
    db.refresh(db_email_important)
    return db_email_important


def create_email_important_bulk(
    db: Session, email_important_list: List[EmailImportantSchema]
):
    for email_important in email_important_list:
        if email_important.is_important:
            db_email_important = EmailImportantModel(**email_important.model_dump())
            db.merge(db_email_important)
    db.commit()


def create_todo(db: Session, todo: TodoSchema):
    db_todo = TodoModel(**todo.model_dump(), id=str(uuid.uuid4()))
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def create_todos_bulk(db: Session, todos: List[TodoSchema]):
    db_todos = [TodoModel(**todo.model_dump(exclude_none=True)) for todo in todos]
    db.add_all(db_todos)
    db.commit()
    for db_todo in db_todos:
        db.refresh(db_todo)
    return TodoList(todo=[TodoSchema.model_validate(db_todo) for db_todo in db_todos])


def get_emails(db: Session):
    db_emails = db.query(EmailModel).all()
    return [EmailSchema.model_validate(db_email) for db_email in db_emails]


def get_email(db: Session, email_id: str):
    db_email = db.query(EmailModel).filter(EmailModel.id == email_id).first()
    return EmailSchema.model_validate(db_email) if db_email else None


def get_email_important(db: Session, email_id: str):
    db_email_important = (
        db.query(EmailImportantModel).filter(EmailImportantModel.id == email_id).first()
    )
    return (
        EmailImportantSchema.model_validate(db_email_important)
        if db_email_important
        else None
    )


def get_email_important_bulk(db: Session):
    db_email_important_list = (
        db.query(EmailImportantModel)
        .join(EmailModel, EmailModel.id == EmailImportantModel.id)
        .all()
    )
    return [
        EmailImportantSchema.model_validate(db_email_important)
        for db_email_important in db_email_important_list
    ]


def get_important_emails(db: Session):
    important_emails = (
        db.query(EmailModel)
        .join(EmailImportantModel, EmailModel.id == EmailImportantModel.id)
        .all()
    )
    return [EmailSchema.model_validate(email) for email in important_emails]


def get_todos(db: Session) -> TodoList:
    db_todos = db.query(TodoModel).filter(TodoModel.is_deleted == False).all()
    print(db_todos)
    return TodoList(todo=[TodoSchema.model_validate(db_todo) for db_todo in db_todos])


def update_priority_ratings(
    db: Session, important_response: List[EmailImportantSchema]
):
    for email_important in important_response:
        stmt = (
            update(EmailModel)
            .where(EmailModel.id == email_important.id)
            .values(priority_rating=email_important.priority_rating)
        )
        db.execute(stmt)
    db.commit()


def update_email_summaries(db: Session, email_summaries: List[EmailSummary]):
    for email_summary in email_summaries:
        stmt = (
            update(EmailModel)
            .where(EmailModel.id == email_summary.id)
            .values(summary=email_summary.summary)
        )
        db.execute(stmt)
    db.commit()


def update_email_summary(db: Session, email_summary: EmailSummary):
    stmt = (
        update(EmailModel)
        .where(EmailModel.id == email_summary.id)
        .values(summary=email_summary.summary)
    )
    db.execute(stmt)
    db.commit()


def set_todo_completed(db: Session, todo_id: int):
    stmt = update(TodoModel).where(TodoModel.id == todo_id).values(is_completed=True)
    db.execute(stmt)
    db.commit()


def set_todo_deleted(db: Session, todo_id: int):
    stmt = update(TodoModel).where(TodoModel.id == todo_id).values(is_deleted=True)
    db.execute(stmt)
    db.commit()


def delete_all_todos(db: Session):
    stmt = update(TodoModel).values(is_deleted=True)
    db.execute(stmt)
    db.commit()


def delete_email_by_id(db: Session, email_id: str):
    stmt = delete(EmailModel).where(EmailModel.id == email_id)
    db.execute(stmt)
    db.commit()


def delete_all_emails(db: Session):
    stmt = delete(EmailModel)
    db.execute(stmt)
    db.commit()
