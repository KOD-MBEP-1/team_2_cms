ACCEPTED_PSQL_TYPES = (str, int, float, bool, dict)


def get_key_name_value(dict_items: list[tuple[str, str]]) -> dict:
    """
    Function returning a tuple with two dictionaries, one with the names of the
    keys and other with key, value
    """

    key_name_dict = {f"{key}_name": key for (key, value) in dict_items}

    return key_name_dict


def get_string_named_argument(x: str):
    "Function to return a list of psycopg named arguments"
    return f"%({x})s"


def get_named_arguments(some_iter: iter) -> list[str]:
    "Function to return psycopg named arguments format from an iter. Ready to insert into a query"
    return get_comma_string(map(get_string_named_argument, some_iter))


def get_comma_string(some_iterable: iter) -> str:
    """
    Function returning a tuple with two dictionaries, one with the names of the
    keys and other with key, value
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
    """Function returning a list of filtered entities"""

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
