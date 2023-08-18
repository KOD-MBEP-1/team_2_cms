def get_key_name_value(dict_items: list[tuple[str, str]]) -> dict:
    """
    Function returning a tuple with two dictionaries, one with the names of the
    keys and other with key, value
    """

    key_name_dict = {f"{key}_name": key for (key,) in dict_items}

    return key_name_dict


def get_string_named_argument(x: str):
    "Function to return a list of psycopg named arguments"
    return f"$({x})s"


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

    dict_items = [(key, val) for key, val in some_dict.items()]

    # This types are arbitrary. Representing the types accepted in postgresql fields

    filtered_entities = filter(
        lambda key, value: isinstance(value, (str, int, float, bool, dict)), dict_items
    )

    return filtered_entities
