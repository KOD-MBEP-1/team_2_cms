import psycopg

DB_CONNECTION_STRING = f"dbname={DB_NAME} user={DB_USER} host={DB_HOST}"


def get_connection_and_cursor():
    # cursor.execute(
    #     """
    #     CREATE TABLE test (
    #         id serial PRIMARY KEY,
    #         num integer,
    #         data text)
    #     """
    # )

    # # Pass data to fill a query placeholders and let Psycopg perform
    # # the correct conversion (no SQL injections!)
    # cursor.execute(
    #     "INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def")
    # )

    # # Query the database and obtain data as Python objects.
    # The new db connection
    # cursor.execute("SELECT * FROM test")
    # cursor.fetchone()
    # # will return (1, 100, "abc'def")

    # # You can use `cursor.fetchmany()`, `cursor.fetchall()` to return a list
    # # of several records, or even iterate on the cursorsor
    # for record in cursor:
    #     print(record)

    # # Make the changes to the database persistent
    # connection.commit()

    return connection


def run_select(col, table, where, order_by):
    with psycopg.connect(DB_CONNECTION_STRING) as connection:
        print("DB connected")

        with connection.cursor() as cursor:
            columns_string = ", ".join(col) if isinstance(col, tuple) else col
            where_string = " " + where if isinstance(where, str) else "True"
            order_by_command = (
                f"ORDER BY {order_by}" if isinstance(order_by, str) else ""
            )

            cursor.execute(
                f"SELECT {columns_string} FROM {table} WHERE{where_string} {order_by_command};"
            )

            result = cursor.fetchall()

            return result


def run_insert(table, entity: dict, return_cols="*"):
    with psycopg.connect(DB_CONNECTION_STRING) as connection:
        print("DB connected")

        with connection.cursor() as cursor:
            cols = ", ".join(entity.keys())
            list_values = entity.values()

            binded_values = ", ".join(map(lambda: "%s", list_values))

            query = f"INSERT INTO {table}({cols}) VALUES({binded_values}) RETURNING {return_cols};"

            result = cursor.execute(query, list_values)

            connection.commit()

            print(f"One entity inserted {result}")

            return result


def run_update(table, updated_entity: dict, where, return_cols="*"):
    with psycopg.connect(DB_CONNECTION_STRING) as connection:
        print("DB connected")

        with connection.cursor() as cursor:
            entity_entries = [(key, val) for key, val in updated_entity.items()]

            filtered_entities = filter(
                lambda entry: isinstance(entry[1], str), entity_entries
            )

            entity_set_values = ", ".join(
                map(lambda entry: f"{entry[0]} = {entry[1]}", filtered_entities)
            )

            where_command = where if isinstance(where, str) else "false"

            query = f"UPDATE {table} SET {entity_set_values} WHERE {where_command} RETURNING {return_cols};"

            result = cursor.execute(query)

            connection.commit()

            print(f"One entity updated {result}")

            return result


def run_delete(table, where, return_cols="*"):
    with psycopg.connect(DB_CONNECTION_STRING) as connection:
        print("DB connected")

        with connection.cursor() as cursor:
            where_command = where if isinstance(where, str) else "false"

            query = (
                f"DELETE FROM {table} WHERE {where_command} RETURNING {return_cols};"
            )

            result = cursor.execute(query)

            connection.commit()

            print(f"One entity deleted {result}")

            return result
