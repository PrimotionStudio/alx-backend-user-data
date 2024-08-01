#!/usr/bin/env python3
"""
This module contains the function to obfuscate logs.
"""
import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log_msg = super(RedactingFormatter, self).format(record)
        filtered = filter_datum(list(self.fields),
                                RedactingFormatter.REDACTION,
                                record.msg, RedactingFormatter.SEPARATOR)
        return re.sub(record.msg, filtered, log_msg)


def filter_datum(fields, redaction, message, separator):
    """
    This function filters the data from the log message.
    """
    for p in re.split(";", message):
        field = re.split("=", p)
        if field[0] in fields:
            message = re.sub(f"{field[0]}={field[1]}",
                             f"{field[0]}={redaction}", message)
    return message
