import imaplib
import email
import logging
import time
from typing import List

from app.config.settings import (
    IMAP_HOST,
    IMAP_USER,
    IMAP_PASS,
    IMAP_FOLDER,
    IMAP_MAX_RETRIES,
    IMAP_RETRY_DELAY_SEC,
)

logger = logging.getLogger(__name__)


class ImapClient:
    def __init__(
        self,
        host: str = IMAP_HOST,
        user: str = IMAP_USER,
        password: str = IMAP_PASS,
        folder: str = IMAP_FOLDER,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.folder = folder

    def _connect(self) -> imaplib.IMAP4_SSL:
        last_exc: Exception | None = None

        for attempt in range(1, IMAP_MAX_RETRIES + 1):
            try:
                logger.info(
                    f"IMAP connect attempt {attempt} to {self.host} as {self.user}"
                )
                mail = imaplib.IMAP4_SSL(self.host)
                mail.login(self.user, self.password)
                logger.info("IMAP connected successfully")
                return mail
            except Exception as e:
                last_exc = e
                logger.error(
                    f"IMAP connect failed on attempt {attempt}: {e!r}"
                )
                if attempt < IMAP_MAX_RETRIES:
                    time.sleep(IMAP_RETRY_DELAY_SEC)

        logger.error("IMAP connection failed after all retries")
        if last_exc:
            raise last_exc
        else:
            raise RuntimeError("IMAP connection failed for unknown reason")

    def fetch_unseen(self) -> List[email.message.Message]:
        mail = self._connect()

        try:
            status, _ = mail.select(self.folder)
            if status != "OK":
                logger.error(f"Failed to select folder {self.folder}: {status}")
                return []

            status, data = mail.search(None, "UNSEEN")
            if status != "OK":
                logger.error(f"IMAP search UNSEEN failed: {status}")
                return []

            messages: List[email.message.Message] = []
            ids = data[0].split()
            logger.info(f"Found {len(ids)} unseen messages")

            for num in ids:
                status, msg_data = mail.fetch(num, "(RFC822)")
                if status != "OK":
                    logger.error(f"IMAP fetch failed for {num}: {status}")
                    continue

                msg = email.message_from_bytes(msg_data[0][1])
                messages.append(msg)

                # помечаем письмо прочитанным
                mail.store(num, "+FLAGS", "\\Seen")

            return messages
        finally:
            try:
                mail.close()
            except Exception:
                # папка может быть не открыта — не страшно
                pass
            mail.logout()
