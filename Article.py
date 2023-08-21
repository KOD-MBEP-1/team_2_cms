from DB_entity import DB_Entity


class Article(DB_Entity):
    def __init__(self):
        super().__init__("article", "articles")

    def create(self, author_id, category_id, title, content, is_active=True):
        "Create article"
        self.create_item(
            {
                "author_id": author_id,
                "category_id": category_id,
                "title": title,
                "content": content,
                "is_active": is_active,
            }
        )

    def update(self, author_id, category_id, title, content, is_active, article_id):
        "update article"
        self.update_item(
            {
                "author_id": author_id,
                "category_id": category_id,
                "title": title,
                "content": content,
                "is_active": is_active,
            },
            article_id,
        )

    def get_one(self, article_id):
        "Get one article by id"
        if not isinstance(article_id, (str, int, float)):
            raise TypeError("You need to provide a valid article_id")

        self.get_item_by_id(
            article_id,
        )

    def deactivate_articles(self, articles_id):
        "Deactivate a list of articles by id"
        if isinstance(articles_id, (list, tuple)):
            for article in articles_id:
                self.deactivate_article(article)

    def deactivate_article(self, article_id):
        "Deactivate one article by id"
        self.update_item(
            {
                "is_active": False,
            },
            article_id,
        )

    def get_articles_by_foreign_key(self, table_name: str):
        "Get articles"
        self.get_items_with_join(
            "*",
            ("true", "is", "true"),
            {
                "type": "RIGHT JOIN",
                "table_name": table_name,
                "alias": f"{table_name[0]}{table_name[1]}",
                "fk": f"{table_name}_id",
                "pk": "article_id",
            },
        )

    def get_articles_by_one_foreign_key(self, table_name: str, foreign_key_id: str):
        "Get articles"
        self.get_items_with_join(
            "*",
            (f"{table_name[0]}{table_name[1]}.{table_name}_id", "=", foreign_key_id),
            {
                "type": "RIGHT JOIN",
                "table_name": table_name,
                "alias": f"{table_name[0]}{table_name[1]}",
                "fk": f"{table_name}_id",
                "pk": "article_id",
            },
        )
