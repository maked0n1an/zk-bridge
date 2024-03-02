import inspect
import logging
import os
import sys
from pathlib import Path


class CustomLogger:
    FOLDER_NAME: str = 'logs'
    LOGGERS: dict[str, logging.Logger] = {}

    def __init__(
        self,
        account_id: str | int,
        address: str,
        network: str,
        create_log_file_per_account: bool = False
    ) -> None:
        self.account_id = account_id
        self.address = address
        self.network = network
        self.create_log_file_per_account = create_log_file_per_account
        if create_log_file_per_account:
            self._create_log_folder()

    @classmethod
    def _create_log_folder(cls):
        relative_path = Path(cls.FOLDER_NAME)
        relative_path.mkdir(parents=True, exist_ok=True)

    def get_logging_format(self) -> dict:
        log_format_dict = {
            'log_format': (
                CustomLogDataAndRecord.LOG_TIME 
                + CustomLogDataAndRecord.LOG_LEVELNAME_FORMAT
                + CustomLogDataAndRecord.LOG_MESSAGE
            ),
            'datafmt': '%Y-%m-%d %H:%M:%S'
        }

        return log_format_dict

    def _initialize_main_log(self) -> logging.Logger:
        if 'main_logger' not in self.LOGGERS:
            main_logger = logging.getLogger("main")
            main_logger.setLevel(logging.DEBUG)
            log_format_dict = self.get_logging_format()

            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(logging.Formatter(
                log_format_dict['log_format'],
                datefmt=log_format_dict['datafmt']
            ))
            main_logger.addHandler(console_handler)

            file_handler = logging.FileHandler(f"main.log")
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(logging.Formatter(
                log_format_dict['log_format'],
                datefmt=log_format_dict['datafmt']
            ))
            main_logger.addHandler(file_handler)
            main_logger.handlers[0].setFormatter(
                CustomLogDataAndRecord(log_format_dict['log_format'])
            )

            logging.addLevelName(26, "SUCCESS")
            logging.addLevelName(28, "MINTED")

            self.LOGGERS["main_logger"] = main_logger

        return self.LOGGERS["main_logger"]

    def _initialize_account_log(self, account_id: str) -> logging.Logger:
        if account_id not in self.LOGGERS:
            wallet_logger = logging.getLogger(
                f'{self.FOLDER_NAME}/log_{account_id}'
            )
            wallet_logger.setLevel(logging.DEBUG)
            log_format_dict = self.get_logging_format()

            file_handler = logging.FileHandler(
                f"{self.FOLDER_NAME}/log_{account_id}.log"
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(CustomAccountLogFormatter(
                log_format_dict['log_format'],
                datefmt=log_format_dict['datafmt']
            ))
            wallet_logger.addHandler(file_handler)

            self.LOGGERS[account_id] = wallet_logger

        return self.LOGGERS[account_id]

    def log_message(self, level: str, message: str) -> None:
        caller_frame = inspect.currentframe().f_back
        calling_line = f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno}"
        message_with_calling_line = f"{calling_line} - {message}"
        extra = {
            "account_id": self.account_id,
            "address": self.address,
            "network": self.network
        }

        main_logger = self._initialize_main_log()
        main_logger.log(
            level=logging.getLevelName(level),
            msg=message_with_calling_line,
            extra=extra
        )

        if self.create_log_file_per_account:
            logger = self._initialize_account_log(self.account_id)
            logger.log(
                level=logging.getLevelName(level),
                msg=message_with_calling_line,
                extra=extra
            )


class CustomLogFormattedRecord(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.root_folder = os.getcwd()
        super().__init__(*args, **kwargs)

    def format_message(self, record: logging.LogRecord) -> logging.LogRecord:
        pathname_with_msg = record.msg
        if pathname_with_msg.startswith(self.root_folder):
            pathname_with_msg = os.path.relpath(
                pathname_with_msg, self.root_folder
            )
        record.msg = pathname_with_msg
        return record


class CustomAccountLogFormatter(CustomLogFormattedRecord):
    def format(self, record):
        record = self.format_message(record)

        return super().format(record)


class CustomLogDataAndRecord(CustomLogFormattedRecord):
    LOG_TIME = '%(asctime)s |'
    LOG_LEVELNAME_FORMAT = ' %(levelname)-8s '
    LOG_MESSAGE = '| %(account_id)8s | %(address)s | %(network)s - %(message)s'

    RED = "\x1b[31;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    BLUE = "\x1b[34;20m"
    WHITE = "\x1b[37;20m"
    GREY = "\x1b[38;20m"
    RESET = "\x1b[0m"

    FORMATS = {
        'DEBUG': BLUE + LOG_LEVELNAME_FORMAT + RESET,
        'INFO': WHITE + LOG_LEVELNAME_FORMAT + RESET,
        'WARNING': YELLOW + LOG_LEVELNAME_FORMAT + RESET,
        'SUCCESS': GREEN + LOG_LEVELNAME_FORMAT + RESET,
        'ERROR': RED + LOG_LEVELNAME_FORMAT + RESET,
        'MINTED': GREEN + LOG_LEVELNAME_FORMAT + RESET
    }

    def format(self, record):
        record = self.format_message(record)

        levelname = record.levelname
        if levelname in self.FORMATS:
            formatted_message = self.LOG_TIME + \
                self.FORMATS[levelname] + self.LOG_MESSAGE
            formatter = logging.Formatter(formatted_message)

        return formatter.format(record)


class ConsoleLoggerSingleton:
    _instance = None

    @staticmethod
    def get_logger():
        if ConsoleLoggerSingleton._instance is None:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            ConsoleLoggerSingleton._instance = logger
        
        return ConsoleLoggerSingleton._instance
