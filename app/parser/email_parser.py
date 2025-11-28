# app/parser/email_parser.py
from email.header import decode_header
from email.utils import parseaddr
from typing import Optional

import email

from app.models.email_dto import EmailData


def decode_header_safe(value: Optional[str]) -> str:
    if not value:
        return ""
    parts = decode_header(value)
    result = []
    for text, enc in parts:
        if isinstance(text, bytes):
            result.append(text.decode(enc or "utf-8", errors="ignore"))
        else:
            result.append(text)
    return "".join(result)


def extract_text_body(msg: email.message.Message) -> str:
    # пробуем вытащить text/plain
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdisp = str(part.get("Content-Disposition") or "")
            if ctype == "text/plain" and "attachment" not in cdisp:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="ignore")

        # если нет text/plain — берем html
        for part in msg.walk():
            ctype = part.get_content_type()
            cdisp = str(part.get("Content-Disposition") or "")
            if ctype == "text/html" and "attachment" not in cdisp:
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="ignore")
        return ""
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="ignore")
        return ""


def clean_body(raw: str) -> str:
    if not raw:
        return ""
    lines = raw.splitlines()
    result = []

    stop_phrases = [
        "On ",                      # On Mon, ...
        "-----Original Message-----",
        "От:",                      # русские реплай-заголовки
    ]

    for line in lines:
        stripped = line.strip()
        if any(stripped.startswith(p) for p in stop_phrases):
            break
        if stripped.startswith(">"):
            break
        result.append(line)

    return "\n".join(result).strip()


def get_thread_id(msg: email.message.Message) -> Optional[str]:
    in_reply_to = msg.get("In-Reply-To")
    if in_reply_to:
        return in_reply_to.strip()

    references = msg.get("References")
    if references:
        refs = references.strip().split()
        if refs:
            return refs[-1]
    return None


def parse_email(msg: email.message.Message) -> EmailData:
    """
    Превращает сырое письмо в EmailData.
    Все доп. поля (status, category, reason, deadline_time, formality)
    сейчас оставляем по умолчанию.
    """
    message_id = (msg.get("Message-ID") or "").strip()

    subject = decode_header_safe(msg.get("Subject"))
    raw_body = extract_text_body(msg)
    cleaned = clean_body(raw_body)

    from_header = msg.get("From") or ""
    to_header = msg.get("To") or ""

    _, from_addr = parseaddr(from_header)
    _, to_addr = parseaddr(to_header)

    return EmailData(
        message_id=message_id,
        thread_id=get_thread_id(msg),
        from_email=from_addr or None,
        to_email=to_addr or None,
        subject=subject or None,
        raw_body=raw_body or None,
        cleaned_body=cleaned,
        # status, category, reason, deadline_time, formality
        # будут взяты из дефолтов модели
    )
