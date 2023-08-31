#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List


def filter_datum(fields: List, redaction: str,
                 message: str, separator: str) -> str:
    """
        This func replaces a matching str in another string with a specific str
    """
    return re.sub(rf"({'|'.join(fields)})=[^{separator}]*",
                  rf"\1={redaction}", message)
