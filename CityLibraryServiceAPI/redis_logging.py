import logging
import os
from datetime import datetime

from dotenv import load_dotenv
from redis import Redis
from redis_om import HashModel

load_dotenv()

redis_client = Redis(
    host=os.getenv("REDIS_HOST"),
    port=6379,
    db=1,
    decode_responses=True,
)


class Log(HashModel):
    level = str
    message = str
    timestamp = datetime
    metadata = dict

    class Meta:
        database = redis_client


class RedisLogHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        exc_info = None
        if record.exc_info:
            exc_info = self.formatException(record.exc_info)
        log = Log(
            level=record.levelname,
            message=record.getMessage(),
            timestamp=datetime.fromtimestamp(record.created),
            metadata={
                "name": record.name,
                "pathname": record.pathname,
                "lineno": record.lineno,
                "funcName": record.funcName,
                "exc_info": exc_info,
            }
        )
        log.save()
