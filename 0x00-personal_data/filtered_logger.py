#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List
import logging
import os
import mysql.connector


# Define PII_FIELDS tuple
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "{HOLBERTON} %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """The constructor function that accepts fields and calls the
        super class constructor to initialize the child class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields if fields else PII_FIELDS

    def format(self, record: logging.LogRecord) -> List[str]:
        """Formats the specified log record as text.
        Filters values in incoming log record using filter_datum"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
        This func replaces a matching str in another string with a specific str
    """
    return re.sub(rf"({'|'.join(fields)})=[^{separator}]*",
                  rf"\1={redaction}", message)


def get_logger() -> logging.Logger:
    """
    This function creates a Logger and a streamhandler for that logger

    The function also defines propagation to prevent the logger from
    propagating log messages to the parent logger

    Returns:
        This function returns a logging.logger object
    """
    logger = logging.getLogger('user_data')  # Create logger

    logger.setLevel(logging.INFO)  # set logger level

    logger.propagate = False  # Prevent propagation

    stream_handler = logging.StreamHandler()  # Create streamhandler

    # create a redactingFormatter and set it for the handler
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db():
    """This function attempts to establish a connection with MySQL Db
    by getting variables stored in the shell environment and using them
    as credentials to login to the database
    """
    # Get db credentials from environment variables
    db_username = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')

    # Create a MySQL connection
    try:
        connection = mysql.connector.connect(
                user=db_username,
                password=db_password,
                host=db_host,
                database=db_name
                )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def main() -> None:
    """This function obtains a db connection using get_db, retrieves all
    rows and in the user while filtering the rows with a specific format
    """

    logger = get_logger()
    db_connection = get_db()

    if db_connection:
        try:
            cursor = db_connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users")

            # Fetch all rows
            rows = cursor.fetchall()

            # Log the filtered rows
            for row in rows:
                # Create a log message using the desired format
                log_message = (
                        f"name={RedactingFormatter.REDACTION}; "
                        f"email={RedactingFormatter.REDACTION}; "
                        f"phone={RedactingFormatter.REDACTION}; "
                        f"ssn={RedactingFormatter.REDACTION}; "
                        f"password={RedactingFormatter.REDACTION}; "
                        f"ip={row['ip']}; "
                        f"last_login={row['last_login']}; "
                        f"user_agent={row['user_agent']}; "
                        )
                # Log the info
                logger.info(log_message)
        except Exception as e:
            logger.error(f"Error retrieving data: {str(e)}")
        finally:
            cursor.close()
            db_connection.close()


if __name__ == '__main__':
    main()
