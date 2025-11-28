import re
from email.utils import parseaddr
from email.header import decode_header
from app.models.email_dto import EmailData


def decode_header_safe(value: str) -> str:
    if not value:
        return ""
    parts = decode_header(value)
    out = []
    for text, enc in parts:
        if isinstance(text, bytes):
            out.append(text.decode(enc or "utf-8", errors="ignore"))
        else:
            out.append(text)
    return "".join(out)


def html_to_text(html: str) -> str:
    # Простейшая очистка HTML → только текст
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)      # убираем все теги
    text = text.replace("&nbsp;", " ")
    text = text.strip()
    return text


def extract_text_body(msg):
    # взять text/plain
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(part.get_content_charset() or "utf-8", errors="ignore")

        # Если plain нет → используем HTML и чистим
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                payload = part.get_payload(decode=True)
                if payload:
                    html = payload.decode(part.get_content_charset() or "utf-8", errors="ignore")
                    return html_to_text(html)
    else:
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


def parse_email(msg):
    # Извлекаем письмо в текстовом виде
    body = extract_text_body(msg)

    _, from_addr = parseaddr(msg.get("From"))
    _, to_addr = parseaddr(msg.get("To") or "")

    return EmailData(
        message_id=msg.get("Message-ID"),
        thread_id=get_thread_id(msg),

        from_email=from_addr,
        to_email=to_addr or None,

        subject=decode_header_safe(msg.get("Subject")),
        raw_body=body,              # теперь здесь только текст, а не html
        cleaned_body=body.strip(),  # можно делать доп. очистку

        status="new"
    )
