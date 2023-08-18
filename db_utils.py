import psycopg

from env_vars import DB_USER, DB_HOST, DB_NAME

DB_CONNECTION_STRING = f"dbname={DB_NAME} user={DB_USER} host={DB_HOST}"

def get_connection_and_cursor()->list[psycopg.Connection,psycopg.Cursor]:
    """Function returning Pyscopg cursor and psycopg connection"""
    connection = psycopg.connect(DB_CONNECTION_STRING)
    cursor = connection.cursor()
    return [connection, cursor]

def open_db_connection(func):
    """Decorator for open connection and cursor"""
    def wrapper(*args):
        [conn, curs] = get_connection_and_cursor()
        func(conn,curs,*args)
        
        curs.close()
        conn.close()

    return wrapper
