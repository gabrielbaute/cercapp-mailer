"""Module for configuring logging"""

from typing import Optional

import logging
import os

class LoggerConfig:

    LOG_DIR = "logs"
    LOG_FILE = os.path.join(LOG_DIR, "cercapp_mail.log")
    
    @classmethod
    def setup(cls, level: Optional[int] = None):
        """Initialize the logging system with file and console handlers.
        
        Sets up logging configuration with appropriate formatters and handlers.
        Creates the log directory if it doesn't exist and configures both
        file logging and optional console output for debug mode.
        
        Args:
            level: Optional logging level override. If None, uses environment setting
        """
        os.makedirs(cls.LOG_DIR, exist_ok=True)

        log_level = level if level is not None else "INFO"

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[
                logging.FileHandler(cls.LOG_FILE),
                logging.StreamHandler()
            ],
        )