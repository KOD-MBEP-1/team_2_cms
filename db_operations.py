from typing import NewType, Tuple
import psycopg
import db_utils
import utilities

WhereType = NewType("WhereType", Tuple[str, str, str])


@db_utils.get_connection_and_cursor
def run_select(
    conn: psycopg.Connection,
    curs: psycopg.Cursor,
    table: str,
    col: str,
    where: WhereType,
    order_by: str,
    get_all: bool = False,
):
    """Function to execute a SELECT command"""
    columns_string = ", ".join(col) if isinstance(col, tuple) else col

    where_command = (
        f"WHERE {where[0]} {where[1]} {where[2]}"
        if isinstance(where, WhereType)
        else ""
    )

    order_by_command = f"ORDER BY {order_by}" if isinstance(order_by, str) else ""

    curs.execute(
        f"SELECT {columns_string} FROM {table} {where_command} {order_by_command};"
    )

    result = curs.fetchall() if get_all is True else curs.fetchone()

    return result


@db_utils.get_connection_and_cursor
def run_insert(
    conn: psycopg.Connection,
    curs: psycopg.Cursor,
    table: str,
    entity: dict,
    return_cols: str = "*",
):
    """Function to execute an INSERT command in psql"""
    (key_name_dict, key_value_dict) = utilities.get_entity_key_name_tuple(entity)

    # It's necessary to convert the entry dict into entries so we can get the key_names inside
    # The key_name dict will be use to create named argument placeholders
    # To expand please check: https://www.psycopg.org/psycopg3/docs/basic/params.html#execute-arguments

    entity_col_named_arguments = utilities.get_named_arguments(key_name_dict.keys())

    entity_values_named_arguments = utilities.get_named_arguments(key_value_dict.keys())

    named_arguments_dict = key_name_dict.update(key_value_dict)

    query = f"INSERT INTO {table}({entity_col_named_arguments}) VALUES({entity_values_named_arguments}) RETURNING {return_cols};"

    result = curs.execute(query, named_arguments_dict)

    conn.commit()

    print(f"One entity updated {result}")

    return result


@db_utils.get_connection_and_cursor
def run_update(
    conn: psycopg.Connection,
    curs: psycopg.Cursor,
    table: str,
    entity: dict,
    where: WhereType,
    return_cols: str = "*",
):
    """Function to execute an INSERT command in psql"""

    filtered_entries = utilities.get_filtered_items(entity)

    # Returning a list of strings. Syntax of a SET command but with named arguments

    filtered_entries_list = map(
        lambda key, value: f"{key} = {utilities.get_string_named_argument(value)}",
        filtered_entries,
    )

    set_command = utilities.get_comma_string(filtered_entries_list)

    where_command = (
        f"WHERE {where[0]} {where[1]} {where[2]}"
        if isinstance(where, WhereType)
        else ""
    )

    named_arg_values = {key: val for (key, val) in filtered_entries}

    query = f"UPDATE {table} SET {set_command} WHERE {where_command} RETURNING {return_cols};"

    result = curs.execute(query, named_arg_values)

    conn.commit()

    print(f"One entity updated {result}")

    return result
