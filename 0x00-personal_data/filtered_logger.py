#!/usr/bin/env python3

""" import logging and annotation helpers """
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str,
                 separator: str) -> str:
    """ returns obfuscated log message based on fields"""
    for x in message.split(separator):
        for y in fields:
            if y in x:
                message = re.sub(f'{y}=.*?;', f'{y}={redaction};',
                                 message)
    return message
