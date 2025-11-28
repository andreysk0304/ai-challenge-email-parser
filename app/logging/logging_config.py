# app/logging_config.py
import logging
import sys
import json


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # если нужно, можно добавить больше полей
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)


def setup_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    root.setLevel(level.upper())

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    # очищаем старые хендлеры, если есть
    root.handlers.clear()
    root.addHandler(handler)
