#!/usr/bin/env python3
"""
This module contains the function to obfuscate logs.
"""
import re
import logging
from typing import List, Tuple
import os
import mysql.connector


PII_FIELDS: Tuple[str] = ("email", "phone", "ssn", "password", "ip")


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


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger with specific configuration.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate(False)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """
    Returns a MySQL database connection object.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main():
    """
    Main function to obtain a database connection,
    retrieve all rows in the users table,
    and display each row under a filtered format.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger = get_logger()

    fields = cursor.column_names
    for row in cursor:
        record = "; ".join(f"{field}={value}" for field,
                           value in zip(fields, row)) + ";"
        log_record = logging.LogRecord("user_data", logging.INFO,
                                       None, None, record, None, None)
        logger.handle(log_record)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
