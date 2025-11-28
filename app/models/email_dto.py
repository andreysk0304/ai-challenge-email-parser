from pydantic import BaseModel, EmailStr
from typing import Optional

class ParsedEmail(BaseModel):
    message_id: str
    thread_id: Optional[str] = None

    from_email: EmailStr
    to_email: Optional[EmailStr] = None

    subject: Optional[str] = None

    raw_body: Optional[str] = None
    cleaned_body: str
