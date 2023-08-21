import click
from Article import Article

CURRENT_INSTANCE = None


CATEGORY_ACTIONS = [
    "create",
    "update",
    "get_one",
    "get_all",
    "deactivate",
    "get_author_articles",
    "get_category_articles",
]


@click.command()
@click.option(
    "--action",
    "-a",
    prompt="Select an action to perform on Author table",
    type=click.Choice(CATEGORY_ACTIONS),
    help="Select an action to perform on Author table",
)
@click.option(
    "--author_id",
    prompt=False,
    help="Type the author id of your article",
)
@click.option(
    "--category_id",
    prompt=False,
    help="Type the category_id of your article",
)
@click.option(
    "--title",
    prompt=False,
    help="Type the title of your article",
)
@click.option(
    "--content",
    prompt=False,
    help="Type the content of your article",
)
@click.option(
    "--is_active",
    default=True,
    is_flag=True,
    prompt=False,
    help="Flag to define article state: is_active ",
)
@click.option(
    "--publish_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    prompt=False,
    help="Type the publish_date of the article with the format: YYYY-MM-DD",
)
@click.option(
    "--article_id",
    prompt=False,
    help="Type the article_id you want to refer to",
)
@click.pass_context
def article(ctx, action, **kwargs):
    global CURRENT_INSTANCE
    CURRENT_INSTANCE = Article()
    match action:
        case "create":
            ctx.invoke(create_article, **kwargs)
        case "update":
            ctx.invoke(update_article, **kwargs)
        case "get_one":
            ctx.invoke(get_one_article, **kwargs)
        case "deactivate":
            ctx.invoke(deactivate_article, **kwargs)
        case "get_all":
            ctx.invoke(get_all_articles)
        case "get_author_articles":
            ctx.invoke(get_author_articles)
        case "get_category_articles":
            ctx.invoke(get_category_articles)


@click.command()
def create_article(
    author_id, category_id, title, content, is_active, publish_date, **kwargs
):
    CURRENT_INSTANCE.create(
        author_id, category_id, title, content, is_active, publish_date
    )


@click.command()
def update_article(
    author_id,
    category_id,
    title,
    content,
    publish_date,
    is_active,
    article_id,
    **kwargs,
):
    CURRENT_INSTANCE.update(
        author_id,
        category_id,
        title,
        content,
        is_active,
        publish_date,
        article_id,
    )


@click.command()
def deactivate_article(article_id, **kwargs):
    CURRENT_INSTANCE.deactivate_article(article_id)


@click.command()
def get_one_article(article_id, **kwargs):
    CURRENT_INSTANCE.get_one(
        article_id,
    )


@click.command()
def get_all_articles():
    CURRENT_INSTANCE.get_all()


@click.command()
def get_author_articles(author_id, **kwargs):
    CURRENT_INSTANCE.get_articles_by_one_foreign_key("author", author_id)


@click.command()
def get_category_articles(category_id, **kwargs):
    CURRENT_INSTANCE.get_articles_by_one_foreign_key("category", category_id)
