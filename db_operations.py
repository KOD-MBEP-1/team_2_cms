from typing import Tuple
import psycopg
import db_utils
import utilities

WhereType = Tuple[str, str, str | int | float]


@db_utils.open_db_connection
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

    where_command = utilities.get_where_command(where)

    order_by_command = f"ORDER BY {order_by}" if isinstance(order_by, str) else ""

    curs.execute(
        f"SELECT {columns_string} FROM {table} {where_command} {order_by_command};"
    )

    result = curs.fetchall() if get_all is True else curs.fetchone()

    return result


@db_utils.open_db_connection
def run_insert(
    conn: psycopg.Connection,
    curs: psycopg.Cursor,
    table: str,
    entity: dict,
    return_cols: str = "*",
):
    """Function to execute an INSERT command in psql"""
    (key_name_dict, key_value_dict) = utilities.get_entity_key_name_tuple(entity)

    # It's necessary to convert the entry dict into entries so we can filter them
    # To expand please check: https://www.psycopg.org/psycopg3/docs/basic/params.html#execute-arguments

    entity_col_named_arguments = utilities.get_comma_string(key_value_dict.keys())

    entity_values_named_arguments = utilities.get_named_arguments(key_value_dict.keys())

    query = f"INSERT INTO {table} ({entity_col_named_arguments}) VALUES({entity_values_named_arguments}) RETURNING {return_cols};"

    result = curs.execute(query, key_value_dict)

    created_entity = result.fetchone()

    conn.commit()

    print(f"One entity created {created_entity}")

    return result


@db_utils.open_db_connection
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
        lambda entry: f"{entry[0]} = {utilities.get_string_named_argument(entry[0])}",
        filtered_entries,
    )

    set_command = utilities.get_comma_string(filtered_entries_list)

    where_command = utilities.get_where_command(where)

    named_arg_values = {key: val for (key, val) in filtered_entries}

    query = f"UPDATE {table} SET {set_command} {where_command} RETURNING {return_cols};"

    print(query)
    result = curs.execute(query, named_arg_values)

    entity_updated = result.fetchone()

    conn.commit()

    print(f"One entity updated {entity_updated}")

    return result
