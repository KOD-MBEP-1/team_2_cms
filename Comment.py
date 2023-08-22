from DB_entity import DB_Entity


class Comment(DB_Entity):
    def __init__(self):
        super().__init__("comment", "comments")

    def create(self,content,):
        self.create_item(
            {
                "content": content
            }
        )

    def update(self, comment_id, content):
        self.update_item(
            {
                "name": content
            },
            comment_id,
        )

    def get_one(self, comment_id):
        self.get_item_by_id(
            comment_id,
        )

    def get_comments_by_articles_id(self, article_id):
        self.get_items_with_join(
            "*",
            ("a.article_id", "=", ),
            {
                "type": "LEFT JOIN",
                "table_name": "comments",
                "alias": "c",
                "fk": "article_id",
                "pk": "comment_id",
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
