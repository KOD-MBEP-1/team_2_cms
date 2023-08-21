from DB_entity import DB_Entity


class Author(DB_Entity):
    def __init__(self):
        super().__init__("author", "authors")

    def create(self, name, last_name, email, birthdate):
        self.create_item(
            {
                "name": name,
                "last_name": last_name,
                "email": email,
                "birthdate": birthdate,
            }
        )

    def update(self, author_id, name, last_name, email, birthdate):
        self.update_item(
            {
                "name": name,
                "last_name": last_name,
                "email": email,
                "birthdate": birthdate,
            },
            author_id,
        )

    def get_one(self, author_id):
        self.get_item_by_id(
            author_id,
        )

    def get_articles(self):
        self.get_items_with_join(
            "*",
            True,
            {
                "type": "LEFT JOIN",
                "table_name": "articles",
                "alias": "a",
                "fk": "article_id",
                "pk": "author_id",
            },
        )

    def get_articles_by_author_id(self, author_id):
        self.get_items_with_join(
            "*",
            ("author_id", "=", author_id),
            {
                "type": "LEFT JOIN",
                "table_name": "articles",
                "alias": "a",
                "fk": "article_id",
                "pk": "author_id",
            },
        )
