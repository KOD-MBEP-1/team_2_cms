from DB_entity import DB_Entity


class Category(DB_Entity):
    def __init__(self):
        super().__init__("category", "categories")

    def create(self, name, description):
        self.create_item(
            {
                "name": name,
                "description": description,
            }
        )

    def update(self, category_id, name, description):
        "Update category by id"
        if not isinstance(name, str) or not isinstance(description, str):
            raise TypeError("You need to provide a name or description")

        self.update_item(
            {
                "name": name,
                "description": description,
            },
            category_id,
        )

    def get_one(self, category_id):
        if not isinstance(category_id, (str, int, float)):
            raise TypeError("You need to provide a valid category_id")

        self.get_item_by_id(
            category_id,
        )

    def get_articles_by_category_id(self, category_id):
        self.get_items_with_join(
            "*",
            ("a.category_id", "=", category_id),
            {
                "type": "LEFT JOIN",
                "table_name": "articles",
                "alias": "a",
                "fk": "article_id",
                "pk": "category_id",
            },
        )
