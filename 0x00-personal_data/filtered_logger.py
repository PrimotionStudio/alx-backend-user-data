#!/usr/bin/env python3
"""
This module contains the function to obfuscate logs.
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    This function filters the data from the log message.
    """
    new_str = message
    for p in re.split(";", new_str):
        field = re.split("=", p)
        if field[0] in fields:
            new_str = re.sub(f"{field[0]}={field[1]}", f"{field[0]}={redaction}", new_str)
    return new_str
