import uuid
from sqlalchemy import (
    UUID,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    create_engine,
    JSON,
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import text


def generate_uuid():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class Email(Base):
    __tablename__ = "emails"
    id = Column(String, primary_key=True)
    to = Column(JSON)
    cc = Column(JSON)
    bcc = Column(JSON)
    created = Column(DateTime)
    attachments = Column(JSON)
    importance = Column(String)
    subject = Column(String)
    sender = Column(String)
    content = Column(String)
    priority_rating = Column(Integer)
    summary = Column(String)


class EmailImportant(Base):
    __tablename__ = "email_important"
    id = Column(String, primary_key=True)
    is_important = Column(Boolean)
    is_spam = Column(Boolean)
    important_reason = Column(String)
    spam_reason = Column(String)
    priority_rating = Column(Integer)


class Todo(Base):
    __tablename__ = "todos"
    id = Column(String, primary_key=True, default=generate_uuid, unique=True)
    task = Column(String)
    priority = Column(Integer)
    is_completed = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)


engine = create_engine("sqlite:///emails.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
