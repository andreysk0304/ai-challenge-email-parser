import logging

from app.imap_client.client import ImapClient
from app.parser.email_parser import parse_email
from app.transport.http_client import send_email

logger = logging.getLogger(__name__)


def process_new_emails() -> None:
    logger.info("Starting processing new emails")

    client = ImapClient()
    messages = client.fetch_unseen()

    logger.info(f"Got {len(messages)} messages from IMAP")

    for idx, msg in enumerate(messages, start=1):
        try:
            dto = parse_email(msg)
            logger.info(
                f"[{idx}/{len(messages)}] Parsed email "
                f"message_id={dto.message_id} from={dto.from_email}"
            )
            send_email(dto)
        except Exception as e:
            logger.error(
                f"Failed to process message #{idx}: {e!r}",
                exc_info=True,
            )

    logger.info("Finished processing new emails")
