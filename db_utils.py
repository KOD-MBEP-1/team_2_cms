"""
This module is the declaration of functions that handle the connection and cursors with the
psql server.
"""


import re
import psycopg
from psycopg import sql
from env_vars import DB_USER, DB_HOST, DB_NAME


if (
    not isinstance(DB_USER, str)
    or not isinstance(DB_HOST, str)
    or not isinstance(DB_NAME, str)
):
    raise TypeError(
        "You need to set the right environmental variables. Please refer to .env.example to create your .env file with the correct values"
    )


class DatabaseNotFoundError(Exception):
    """
    Raised when a connection failed with psql because a non-existing database

    PSYCOPG throws a OperationalError which is not meaningfull at all

    Please check: https://www.psycopg.org/psycopg3/docs/api/errors.html#psycopg.OperationalError
    """

    pass


DB_CONNECTION_STRING_NO_DB = f"user={DB_USER} host={DB_HOST}"
DB_CONNECTION_STRING = f"dbname={DB_NAME} user={DB_USER} host={DB_HOST}"


def create_database() -> list[psycopg.Connection, psycopg.Cursor]:
    "Function to create a database and return the connection and cursor"
    conn = psycopg.connect(DB_CONNECTION_STRING_NO_DB)
    conn.autocommit = True

    cursor = conn.cursor()

    # sql module is a safe way to create dynamic queries
    #  SQL class creates sql statements
    # Format method replace placeholders from SQL class: https://www.psycopg.org/psycopg3/docs/api/sql.html#psycopg.sql.SQL.format
    # Same as str.format() but safer for sql commands

    try:
        query = sql.SQL("CREATE DATABASE {db_name} WITH OWNER {db_owner};").format(
            db_name=sql.Identifier(DB_NAME), db_owner=sql.Identifier(DB_USER)
        )

        cursor.execute(query)
    except psycopg.OperationalError as error:
        print(error)
    except Exception as error:
        print("Double check your psql service is running on your machine")
        print(error)

    cursor.close()
    conn.close()


def get_connection_and_cursor() -> list[psycopg.Connection, psycopg.Cursor]:
    """Function returning Pyscopg cursor and psycopg connection"""

    try:
        connection = psycopg.connect(DB_CONNECTION_STRING)
        cursor = connection.cursor()
        return [connection, cursor]

    except psycopg.OperationalError as error:
        is_connection_not_found_error = re.search(
            "^.*database .* does not exist$", str(error)
        )
        if is_connection_not_found_error:
            create_database()
            connection = psycopg.connect(DB_CONNECTION_STRING)
            cursor = connection.cursor()

            return [connection, cursor]


def open_db_connection(func):
    """Decorator for open connection and cursor"""

    def wrapper(*args):
        [conn, curs] = get_connection_and_cursor()
        func(conn, curs, *args)

        curs.close()
        conn.close()

    return wrapper
