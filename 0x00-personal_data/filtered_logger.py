#!/usr/bin/env python3
""" import logging and annotation helpers """
import re
from typing import List
import logging
from os import getenv
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns obfuscated log message based on fields"""
    for y in fields:
        message = re.sub(f'{y}=.*?{separator}', f'{y}={redaction}{separator}',
                         message)
    return message


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ connect to db """
    db_username = getenv("PERSONAL_DATA_DB_USERNAME")
    db_password = getenv("PERSONAL_DATA_DB_PASSWORD")
    db_host = getenv("PERSONAL_DATA_DB_HOST")
    db_name = getenv("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connect(
        host=(db_host, 'localhost'),  # 'localhost
        database=db_name,
        user=(db_username, 'root'),  # 'root'
        password=db_password
    )

    return conn


def main() -> None:
    """ get info from db """
    conn = get_db()
    cursor = conn.cursor()  # create cursor for cmd execution
    cursor.execute("SELECT * FROM users")
    logger = get_logger()
    result = cursor.fetchall()
    for row in result:
        result = ";".join(str(x) for x in row)
        logger.info(result)

    cursor.close()
    conn.close()


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


if __name__ == "__main__":
    main()
