import os

IMAP_HOST = "imap.yandex.ru"
IMAP_USER = "ilin.vladisaw@yandex.ru"

# ИМЯ переменной окружения
# IMAP_PASS = os.getenv("IMAP_PASS")   # значение задаёшь в окружении
IMAP_PASS = "fmokbrjtqakceagn"

IMAP_FOLDER = "parser"                # или "parser", если такая папка реально есть

BACKEND_URL = os.getenv("BACKEND_URL")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

IMAP_MAX_RETRIES = 3
IMAP_RETRY_DELAY_SEC = 2
HTTP_MAX_RETRIES = 3
HTTP_RETRY_DELAY_SEC = 2
