import os

IMAP_HOST = os.getenv("IMAP_HOST", "imap.yandex.ru")
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")
IMAP_FOLDER = os.getenv("IMAP_FOLDER", "INBOX")

BACKEND_URL = os.getenv("BACKEND_URL")

# логирование
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ретраи для IMAP
IMAP_MAX_RETRIES = int(os.getenv("IMAP_MAX_RETRIES", "3"))
IMAP_RETRY_DELAY_SEC = int(os.getenv("IMAP_RETRY_DELAY_SEC", "2"))

# ретраи для HTTP
HTTP_MAX_RETRIES = int(os.getenv("HTTP_MAX_RETRIES", "3"))
HTTP_RETRY_DELAY_SEC = int(os.getenv("HTTP_RETRY_DELAY_SEC", "2"))
