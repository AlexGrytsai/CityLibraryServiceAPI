import logging
import os


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.pathname:
            dir_path = os.path.dirname(record.pathname)
            folder_name = os.path.basename(dir_path)
            record.folder_name = folder_name
        return super(CustomFormatter, self).format(record)
