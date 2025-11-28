import os

IMAP_HOST = "imap.yandex.ru"

IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")

IMAP_FOLDER = "parser"

BACKEND_URL = os.getenv("BACKEND_URL")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

IMAP_MAX_RETRIES = 3
IMAP_RETRY_DELAY_SEC = 2
HTTP_MAX_RETRIES = 3
HTTP_RETRY_DELAY_SEC = 2
