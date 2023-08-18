import psycopg
from typing import NewType,Tuple
import db_utils

WhereType = NewType('WhereType', Tuple[str,str,str])

@db_utils.get_connection_and_cursor
def run_select(conn:psycopg.Connection, curs:psycopg.Cursor, col:str, table:str, where: WhereType, order_by:str, get_all:bool=False):
  """Function to execute a SELECT command"""
  columns_string = ", ".join(col) if isinstance(col, tuple) else col
  
  where_command = f"WHERE {where[0]} {where[1]} {where[2]}" if isinstance(where,WhereType) else ""
  
  order_by_command = (
      f"ORDER BY {order_by}" if isinstance(order_by, str) else ""
  )

  curs.execute(
      f"SELECT {columns_string} FROM {table} {where_command} {order_by_command};"
  )

  result = curs.fetchall() if get_all is True else curs.fetchone()

  return result
  
  
  
@db_utils.get_connection_and_cursor
def run_insert(conn:psycopg.Connection, curs:psycopg.Cursor, col:str, table:str, where: WhereType, order_by:str, get_all:bool=False):
  """Function to execute an INSERT command"""
  columns_string = ", ".join(col) if isinstance(col, tuple) else col
  
  where_command = f"WHERE {where[0]} {where[1]} {where[2]}" if isinstance(where,WhereType) else ""
  
  order_by_command = (
      f"ORDER BY {order_by}" if isinstance(order_by, str) else ""
  )

  curs.execute(
      f"SELECT {columns_string} FROM {table} {where_command} {order_by_command};"
  )

  result = curs.fetchall() if get_all is True else curs.fetchone()

  return result
  
  