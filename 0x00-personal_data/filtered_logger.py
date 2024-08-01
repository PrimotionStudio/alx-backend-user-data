#!/usr/bin/env python3
"""
This module contains the function to obfuscate logs.
"""
import re


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
