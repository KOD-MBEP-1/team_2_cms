"""
This module is the declaration of functions interacting and executing commands 
into the database
"""

from typing import Tuple
import psycopg
from psycopg import sql
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

    print(result)

    return result


@db_utils.open_db_connection

def run_select_with_join(
    conn: psycopg.Connection,
    curs: psycopg.Cursor,
    table: str,
    col: str,
    where: WhereType,
    order_by: str,
    join=None,
    get_all: bool = False,
):
    """Function to execute a SELECT command"""
    columns_string = ", ".join(col) if isinstance(col, tuple) else col

    join_command = (
        utilities.get_join_string(join)
        if isinstance(join, dict)
        else ", ".join([utilities.get_join_string(join_item) for join_item in join])
        if isinstance(join, list)
        else " "
    )

    where_command = utilities.get_where_command(where)

    order_by_command = f"ORDER BY {order_by}" if isinstance(order_by, str) else ""

    curs.execute(
        f"SELECT {columns_string} FROM {table}{join_command} {where_command} {order_by_command};"
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

    return created_entity


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
        lambda entry: f"{entry[0]} = {{}}",
        filtered_entries,
    )

    set_command = utilities.get_comma_string(filtered_entries_list)

    where_command = utilities.get_where_command(where)

    named_arg_values = {key: val for (key, val) in filtered_entries}

    query = f"UPDATE {table} SET {set_command} {where_command} RETURNING {return_cols};"

    print(query)
    result = curs.execute(query, named_arg_values)
    placeholder_values = [sql.Identifier(entry[1]) for entry in filtered_entries]
    where_command = utilities.get_where_command(where)
    print(where, where_command)

    query = (
        sql.SQL(
            f"UPDATE {table} SET {set_command} {where_command} RETURNING {return_cols};"
        )
        .format(*placeholder_values)
        .as_string(conn)
        .replace('"', "'")
    )

    print(query)
    result = curs.execute(
        query,
    )

    entity_updated = result.fetchone()

    conn.commit()

    print(f"One entity updated {entity_updated}")

    return entity_updated


@db_utils.open_db_connection
def create_function_timestamp(
    conn: psycopg.Connection, curs: psycopg.Cursor, table: str
):
    function_query = """
    CREATE OR REPLACE FUNCTION trigger_set_timestamp()
    RETURNS TRIGGER AS $$
    BEGIN
      NEW.updated_at = NOW();
      RETURN NEW;
    END;
      NEW.last_update = NOW();
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """

    curs.execute(function_query)

    trigger_query = f"""
      CREATE TRIGGER set_timestamp_{table}
      BEFORE UPDATE ON {table}
      FOR EACH ROW
      EXECUTE PROCEDURE trigger_set_timestamp();
    """

    curs.execute(trigger_query)


@db_utils.open_db_connection
def run_create_table(
    conn: psycopg.Connection,
    curs: psycopg.Cursor,
    table: str,
    columns: dict[str, tuple],
    constraint: dict,
):
    """Function to execute a CREATE TABLE IF NOT EXIST command in psql"""

    filtered_entries = utilities.get_filtered_items(columns)

    # Returning a list of strings. Syntax of a SET command but with named arguments

    filtered_entries_list = list(
        map(
            lambda entry: f"{entry[0]} {' '.join(entry[1])}",
            filtered_entries,
        )
    )

    col_command = utilities.get_comma_string(filtered_entries_list)

    constraint_string = (
        f"""
        , CONSTAINT {constraint['name']}
          FOREIGN KEY({constraint['col_name']})
            REFERENCES {constraint['table_name'] ({constraint['foreign_col_name']})}
        """
        if isinstance(constraint, dict)
        utilities.get_constaint_string(constraint)
        if isinstance(constraint, dict)
        else ", ".join(
            [
                utilities.get_constaint_string(constraint_item)
                for constraint_item in constraint
            ]
        )
        if isinstance(constraint, (list, tuple))
        else ""
    )

    query = f"CREATE TABLE IF NOT EXISTS {table} ({col_command}{constraint_string});"

    result = curs.execute(query)

    conn.commit()

    print(f"One table created {result}")

    return result
