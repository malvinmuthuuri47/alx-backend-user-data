#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "{HOLBERTON} %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: str):
        """The constructor function that accepts fields and calls the
        super class constructor to initialize the child class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        This function returns the logging format for the message passed
        and calles the filter_datum to handle obfuscation returning the
        output of that function
        """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message,
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
        This func replaces a matching str in another string with a specific str
    """
    return re.sub(rf"({'|'.join(fields)})=[^{separator}]*",
                  rf"\1={redaction}", message)
