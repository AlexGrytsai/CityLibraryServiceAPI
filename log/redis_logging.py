import logging
import os
from typing import Dict, Optional

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
    level: str
    data_time: str
    folder_name: str
    filename: str
    message: str
    metadata: Optional[Dict] = None

    class Meta:
        database = redis_client


class RedisLogHandler(logging.Handler):
    def __init__(self) -> None:
        logging.Handler.__init__(self)

    def emit(self, record):
        level = record.levelname
        data_time = record.asctime
        folder_name = record.folder_name
        filename = record.filename
        message = record.message

        log = Log(
            level=level,
            data_time=data_time,
            folder_name=folder_name,
            filename=filename,
            message=message,
        )
        log.save()
