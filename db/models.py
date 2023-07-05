from pydantic import BaseModel, EmailStr


class EmailData(BaseModel):
    recipient_email: EmailStr
    subject: str
    content: str
    project_name: str
