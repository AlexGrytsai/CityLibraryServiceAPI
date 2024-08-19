import logging

from loggi.models import Log


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
