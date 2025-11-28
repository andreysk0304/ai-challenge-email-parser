from typing import Optional
from pydantic import BaseModel


class ParsedEmail(BaseModel):
    # ID письма
    message_id: str
    # ID письма, на которое это ответ (In-Reply-To / References)
    thread_id: Optional[str] = None

    # просто строки, без строгой валидации email
    from_email: str
    to_email: Optional[str] = None

    subject: Optional[str] = None

    # исходный текст
    raw_body: Optional[str] = None
    # очищенный текст
    cleaned_body: str
