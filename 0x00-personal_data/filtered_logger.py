#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List


def filter_datum(fields: List, redaction: str,
                 message: str, separator: str) -> str:
    """
        This func replaces a matching str in another string with a specific str

        Args:
            fields: A list of strings representing all fields to obfuscate
            redaction: str representing by what the field will be obfuscated
            message: str representing the log line
            separator: sre representation of a char separating fields of the
                       log line
    """
    return re.sub(rf"({'|'.join(fields)})=[^{separator}]*",
                  rf"\1={redaction}", message)
