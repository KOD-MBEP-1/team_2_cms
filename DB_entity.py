"""
Module with the DB Entity class, this class should be a parent class
"""
import os
import db_operations
import utilities


class DB_Entity:
    """
    Class for base DB Tables with basic crud operations
    Please notice that the init method includes the creation
    of the table if not exists
    """

    def __init__(self, table_name: str, schema_file_name: str):
        self.name = table_name
        self.schema_file_name = schema_file_name

        dict_schema = self.get_file_schema()

        constraint = dict_schema.copy()["constraint"]

        if isinstance(constraint, dict):
            del dict_schema["constraint"]

        if isinstance(dict_schema["last_update"], str):
            self.create_updated_at_trigger()

        db_operations.run_create_table(self.name, dict_schema, constraint)

    def get_file_schema(self) -> dict:
        current_path = os.path.dirname(__file__)
        file_name = f"{self.schema_file_name}.json"
        file_path = current_path + f"/{file_name}"
        schema_dict = utilities.read_json_file(file_path)

        dict_schema = {key: tuple(value.split(" ")) for (key, value) in schema_dict}

        return dict_schema

    def create_updated_at_trigger(self):
        db_operations.create_function_timestamp(self.name)

    def get_all(self, col="*", order_by="*"):
        "Method to get all the entities"
        db_operations.run_select(self.name, col, True, order_by, True)

    def get_items_by_column(self, col="*", filter: tuple = (True), order_by="*"):
        db_operations.run_select(self.name, col, filter, order_by, True)

    def get_item_by_column(self, col="*", filter: tuple = (True), order_by="*"):
        db_operations.run_select(self.name, col, filter, order_by, False)

    def get_item_by_id(self, id):
        id_name = f"{self.name}_id"
        db_operations.run_select(self.name, "*", (id_name, "IS", id), id_name, False)

    def update_item(self, entity, id):
        id_name = f"{self.name}_id"
        db_operations.run_update(
            self.name,
            entity,
            (id_name, "IS", id),
        )

    def create_item(self, entity, return_columns="*"):
        db_operations.run_insert(self.name, entity, return_columns)
