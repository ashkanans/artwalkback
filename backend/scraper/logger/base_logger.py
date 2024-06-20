import logging
import os
from datetime import datetime


class BaseLogger:
    def __init__(self):
        # Get scrapper's name
        scrapper_name = self.__class__.__name__
        # Create a folder for scrapper_name
        scrapper_folder = f"logs/{scrapper_name}_logs"
        os.makedirs(scrapper_folder, exist_ok=True)

        self.logger = logging.getLogger(scrapper_name)
        self.logger.setLevel(logging.DEBUG)

        if not any(isinstance(handler, logging.StreamHandler) for handler in self.logger.handlers):
            # Create a console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)

            # Create a formatter and add it to the handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)

            # Add the handler to the logger
            self.logger.addHandler(ch)

        # Create a file handler and set level to debug
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_path = os.path.join(scrapper_folder, f"{scrapper_name}_log_{timestamp}.log")
        fh = logging.FileHandler(log_file_path, encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        # Add the file handler to the logger
        self.logger.addHandler(fh)


