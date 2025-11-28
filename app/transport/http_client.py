import logging
import time

import requests

from app.config.settings import (
    BACKEND_URL,
    HTTP_MAX_RETRIES,
    HTTP_RETRY_DELAY_SEC,
)
from app.models.email_dto import ParsedEmail

logger = logging.getLogger(__name__)


def send_email(dto: ParsedEmail) -> None:
    """
    Отправка письма на backend с ретраями и логами.
    """
    if not BACKEND_URL:
        logger.error("BACKEND_URL is not set, skipping send")
        return

    payload = dto.dict()
    last_exc: Exception | None = None

    for attempt in range(1, HTTP_MAX_RETRIES + 1):
        try:
            logger.info(
                f"Sending email {dto.message_id} to backend "
                f"(attempt {attempt})"
            )
            resp = requests.post(BACKEND_URL, json=payload, timeout=5)

            if resp.status_code < 300:
                logger.info(
                    f"Successfully sent email {dto.message_id}, "
                    f"backend_status={resp.status_code}"
                )
                return

            # если код ответа 4xx/5xx — логируем и пробуем еще раз (кроме явных 4xx, если хочешь)
            logger.error(
                f"Backend responded with {resp.status_code} "
                f"for {dto.message_id}: {resp.text}"
            )

        except Exception as e:
            last_exc = e
            logger.error(
                f"Error sending email {dto.message_id} on attempt {attempt}: {e!r}"
            )

        if attempt < HTTP_MAX_RETRIES:
            time.sleep(HTTP_RETRY_DELAY_SEC)

    logger.error(
        f"Failed to send email {dto.message_id} after "
        f"{HTTP_MAX_RETRIES} attempts"
    )
    if last_exc:
        # можно не кидать исключение, если не хочешь падать
        raise last_exc
