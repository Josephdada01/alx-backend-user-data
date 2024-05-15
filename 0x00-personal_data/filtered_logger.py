#!/usr/bin/env python3
"""
Write a function called filter_datum that returns the log message
obfuscated:
Arguments:
fields: a list of strings representing all fields to obfuscate
redaction: a string representing by what the field will be obfuscated
message: a string representing the log line
separator: a string representing by which character is separating all
fields in the log line (message)
The function should use a regex to replace occurrences of certain field
values.
filter_datum should be less than 5 lines long and use re.sub to perform
the substitution with a single regex.
"""
import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Function to anonymize sensitive information in log files."""
    escaped_fields = '|'.join(re.escape(f) for f in fields)
    pattern = f"({escaped_fields})=([^ {re.escape(separator)}]+)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Mtd to filter values in incoming log records using filter_datum."""
        original_message = record.msg
        redacted_message = filter_datum(self.fields,
                                        self.REDACTION,
                                        original_message, self.SEPARATOR)
        record.msg = redacted_message
        return super(RedactingFormatter, self).format(record)
