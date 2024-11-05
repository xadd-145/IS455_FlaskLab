"""
Configuration file for the Flask application.

Attributes:
    MYSQL_HOST (str): The host name of the MySQL server.
    MYSQL_USER (str): The username to use when connecting to the MySQL server.
    MYSQL_PASSWORD (str): The password to use when connecting to the MySQL server.
    MYSQL_DB (str): The name of the database to use.
    MYSQL_CURSORCLASS (str): The type of cursor to use when connecting to the MySQL server.

    SESSION_TYPE (str): The type of session to use.
    SECRET_KEY (str): The secret key to use for the session.
"""

import os

class Config:
    """
    Configuration class for the Flask application.
    """

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'world' # replace 'world' with your db name
    MYSQL_CURSORCLASS = 'DictCursor'

    # Session Configuration
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
