import time
import logging

from app.config.settings import LOG_LEVEL
from app.logger.logging_config import setup_logging
from app.service.processor import process_new_emails

POLL_INTERVAL = 15  # секунд


def main():
    setup_logging(LOG_LEVEL)
    logger = logging.getLogger(__name__)

    logger.info("Email parser started, polling every %s seconds", POLL_INTERVAL)

    while True:
        try:
            logger.info("Checking for new emails...")
            process_new_emails()
        except Exception as e:
            # Логируем ошибку, но НЕ вылетаем из цикла
            logger.exception(f"Error while processing emails: {e!r}")

        # Ждём 15 секунд до следующей проверки
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()