from email.utils import parseaddr
from app.models.email_dto import ParsedEmail
from app.parser.cleaners import clean_body
from email.header import decode_header


def decode_header_safe(value: str) -> str:
    if not value:
        return ""
    decoded = decode_header(value)
    parts = []
    for text, enc in decoded:
        if isinstance(text, bytes):
            parts.append(text.decode(enc or "utf-8", errors="ignore"))
        else:
            parts.append(text)
    return "".join(parts)


def extract_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(part.get_content_charset() or "utf-8", errors="ignore")
    payload = msg.get_payload(decode=True)
    if payload:
        return payload.decode(msg.get_content_charset() or "utf-8", errors="ignore")
    return ""


def get_thread_id(msg):
    if msg.get("In-Reply-To"):
        return msg.get("In-Reply-To")
    if msg.get("References"):
        refs = msg.get("References").split()
        return refs[-1]
    return None


def parse_email(msg) -> ParsedEmail:
    message_id = msg.get("Message-ID")
    subject = decode_header_safe(msg.get("Subject"))

    raw_body = extract_text(msg)
    cleaned = clean_body(raw_body)

    _, from_addr = parseaddr(msg.get("From"))
    _, to_addr = parseaddr(msg.get("To") or "")

    return ParsedEmail(
        message_id=message_id,
        thread_id=get_thread_id(msg),
        from_email=from_addr,
        to_email=to_addr or None,
        subject=subject,
        raw_body=raw_body,
        cleaned_body=cleaned,
    )
