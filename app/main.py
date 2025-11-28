from app.config.settings import LOG_LEVEL
from app.logging.logging_config import setup_logging
from app.service.processor import process_new_emails


def main():
    setup_logging(LOG_LEVEL)
    process_new_emails()


if __name__ == "__main__":
    main()
