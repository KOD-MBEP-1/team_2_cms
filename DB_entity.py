"""
Module with the DB Entity class, this class should be a parent class
"""

import db_operations


class DB_Entity:
    """
    Class for base DB Tables with basic crud operations
    Please notice that the init method includes the creation
    of the table if not exists
    """

    def __init__(self, name: str, dict_schema: dict):
        self.name = name

        constraint = dict_schema.copy()["constraint"]

        if isinstance(constraint, dict):
            del dict_schema["constraint"]

        db_operations.run_create_table(self.name, dict_schema, constraint)

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
