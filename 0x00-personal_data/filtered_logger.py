#!/usr/bin/env python3

""" import logging and annotation helpers """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns obfuscated log message based on fields"""
    for y in fields:
        if y in message:
            message = re.sub(f'{y}=.*?{separator}', f'{y}={redaction}'
                                                    f'{separator}', message)
    return message
