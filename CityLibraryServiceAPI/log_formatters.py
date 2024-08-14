import logging
import os


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.pathname:
            dir_path = os.path.dirname(record.pathname)
            folder_name = os.path.basename(dir_path)
            print(folder_name)  # utils
            # record.pathname = folder_name
            record.folder_name = folder_name
        return super(CustomFormatter, self).format(record)
