from DB_entity import DB_Entity


class Author(DB_Entity):
    def __init__(self):
        super().__init__("author", "authors")

    def create(self, author_id, article_id, content ):
        self.create_item( 
            {
                    "author_id": author_id,
                    "articles_id": article_id,
                    "content": content,
            }
        )

    def update(self, author_id, article_id, content,comment_id):
        self.update_item(
            {
                "author_id": author_id,
                    "articles_id": article_id,
                    "content": content,
            },
            comment_id,
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
