#!/usr/bin/env python3
""" import logging and annotation helpers """
import re
from typing import List
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "ip")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns obfuscated log message based on fields"""
    for y in fields:
        message = re.sub(f'{y}=.*?{separator}', f'{y}={redaction}{separator}',
                         message)
    return message


def get_logger() -> logging.Logger:
    """ returns logger object"""
    logger = logging.getLogger("user_data")  # create logger with name
    # user_data
    logger.setLevel(logging.INFO)  # set log level
    logger.propagate = False  # prevent log messages from
    # propagating to parent logger
    streamHandler = logging.StreamHandler()  # set stream handler
    # to handle logs from logger
    streamHandler.setFormatter(RedactingFormatter(PII_FIELDS))  # set
    # formatter to handle logs formatting style
    logger.addHandler(streamHandler)  # to mange how logs are handled -
    # streamHandler for stdout,err etc, fileHandler for file
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ OUTPUT THE LOGGED MESSAGE """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return logging.Formatter(fmt=self.FORMAT).format(record)
