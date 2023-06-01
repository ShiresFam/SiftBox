from pydantic import BaseModel

class Email(BaseModel):
    subject: str
    sender: str
    content: str