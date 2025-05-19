import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import seqlog

from src import Config

seqlog.log_to_seq(
    server_url=Config.SEQ_URL.value,
    api_key=None,
    level=Config.LOGGING_LEVEL.value,
    batch_size=5,
    override_root_logger=True
)

logging.getLogger("hdfs.client").level = logging.ERROR


class Logger:
    _instances = {}

    @staticmethod
    def get_logger(
            name: str,
            level: int,
    ) -> logging.Logger:
        """
        Returns a logger instance. Ensures that loggers are reused across the project.

        :param name: Name of the logger.
        :param level: Logging level (e.g., logging.INFO, logging.DEBUG).
        :return: Configured logger instance.
        """
        if name in Logger._instances:
            return Logger._instances[name]

        log_file = os.path.join("logs", "hadoop.log")
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(name)
        logger.setLevel(level)

        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
        console_handler = logging.StreamHandler()

        formatter = CustomFormatter(
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.propagate = True

        Logger._instances[name] = logger
        return logger


class CustomFormatter(logging.Formatter):
    def format(self, record) -> str:
        if 'src' in record.pathname:
            src_index = record.pathname.index('src') + len('src') + 1
            relative_path = record.pathname[src_index:]
            relative_path = relative_path.replace(os.sep, ".").replace(".py", "")
        else:
            relative_path = record.module

        left = f"[{record.levelname}] {self.formatTime(record, self.datefmt)} {relative_path}:{record.lineno}"

        total_width = Config.LOGGER_WIDTH_OFFSET.value
        if len(left) < total_width:
            spaces = " " * (total_width - len(left))
        else:
            spaces = " "

        return f"{left}{spaces}{record.getMessage()}"
