"Utility functions"

import os
import json

ACCEPTED_PSQL_TYPES = (str, int, float, bool, dict, tuple)


def get_key_name_value(dict_items: list[tuple[str, str]]) -> dict:
    """
    Function returning a tuple with two dictionaries, one with the names of the
    keys and other with key, value
    """

    key_name_dict = {f"{key}_name": key for (key, value) in dict_items}

    return key_name_dict


def get_string_named_argument(x: str):
    "Function to return a list of psycopg named arguments as '$(x)s'"
    return f"%({x})s"


def get_named_arguments(some_iter: iter) -> list[str]:
    "Function to return psycopg named arguments format from an iter. Ready to insert into a query"
    return get_comma_string(map(get_string_named_argument, some_iter))


def get_comma_string(some_iterable: iter) -> str:
    """
    Function returning a string with a comma separated items from an iterable
    """

    return ", ".join(some_iterable)


def get_entity_key_name_tuple(dict_entity: dict) -> tuple[dict, dict]:
    """
    Function returning a tuple with two dictionaries, one with the names of the
    keys and other with key, value
    """

    filtered_items = get_filtered_items(dict_entity)
    key_name_dict = get_key_name_value(filtered_items)

    key_value_dict = {key: value for (key, value) in filtered_items}

    return (key_name_dict, key_value_dict)


def get_filtered_items(some_dict: dict) -> list[tuple[str, str]]:
    """Function returning a list of filtered entities, cleaning the values of a dict"""

    dict_items = some_dict.items()
    # This types are arbitrary. Representing the types accepted in postgresql fields

    # Filter returns a filter object, not a list
    filtered_entities = list(
        filter(
            lambda entry: isinstance(entry[1], ACCEPTED_PSQL_TYPES),
            dict_items,
        )
    )

    return filtered_entities


def get_where_command(where: tuple[str]) -> str:
    """
    Function returning where command from a tuple of strings.
    """
    return (
        f"WHERE {where[0]} {where[1]} {where[2]}"
        if isinstance(where, tuple)
        and all(isinstance(where_item, ACCEPTED_PSQL_TYPES) for where_item in where)
        else "WHERE false"
    )


def get_is_file_exist(file_path):
    is_file_exists = os.path.exists(file_path)

    if is_file_exists:
        return True
    else:
        raise FileNotFoundError


def read_json_file(file_path):
    try:
        get_is_file_exist(file_path)

        with open(file_path) as file:
            file_stream = file.read()
            file_content_json = json.loads(file_stream)

            return file_content_json

    except FileNotFoundError as error:
        raise IOError(f"File with path {file_path} doesn't exist") from error

    except PermissionError as error:
        raise IOError(f"You don't have permissions to delete this file") from error


def get_constaint_string(constraint_dict: dict):
    return f"""
        , CONSTAINT {constraint_dict['name']}
          FOREIGN KEY({constraint_dict['col_name']})
            REFERENCES {constraint_dict['table_name'] ({constraint_dict['foreign_col_name']})} ON DELETE CASCADE
        """


def get_join_string(join_command: dict):
    return f"""
            {join_command['type']} {join_command['table_name']} AS {join_command['alias']} ON {join_command['alias']}.{join_command['fk']} = {join_command['pk']} 
        """
