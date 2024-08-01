#!/usr/bin/env python3
"""
This module contains the function to obfuscate logs.
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    This function filters the data from the log message.
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern,
                  lambda x: x.group(0).split('=')[0] + '=' + redaction,
                  message)
