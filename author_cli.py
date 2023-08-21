from Author import Author
import click

CURRENT_INSTANCE = None

TABLE_LIST = [
    "article",
    "author",
    "categories",
]

AUTHOR_ACTIONS = ["create", "get_all", "update", "get_one", "get_articles"]


@click.command()
@click.option(
    "--action",
    "-a",
    prompt="Select an action to perform on Author table",
    type=click.Choice(AUTHOR_ACTIONS),
    help="Select an action to perform on Author table",
)
@click.option(
    "--name",
    prompt=False,
    help="Select an action to perform on Author table",
)
@click.option(
    "--last_name",
    prompt=False,
    help="Type the last name of your new author",
)
@click.option(
    "--email",
    prompt=False,
    help="Type the email of your new author",
)
@click.option(
    "--birthdate",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    prompt=False,
    help="Type the birthdate of your new author with the format: YYYY-MM-DD",
)
@click.option(
    "--author_id",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    prompt=False,
    help="Type the id of your selected author",
)
@click.pass_context
def author(ctx, action, **kwargs):
    global CURRENT_INSTANCE
    CURRENT_INSTANCE = Author()
    match action:
        case "create":
            ctx.invoke(create_author, **kwargs)
        case "update":
            ctx.invoke(update_author, **kwargs)
        case "get_one":
            ctx.invoke(get_one_author, **kwargs)
        case "get_articles":
            ctx.invoke(get_author_articles, **kwargs)
        case "get_all":
            ctx.invoke(get_all_authors)


@click.command()
def create_author(name, last_name, email, birthdate, **kwargs):
    CURRENT_INSTANCE.create(name, last_name, email, birthdate)


@click.command()
def update_author(name, last_name, email, birthdate, author_id, **kwargs):
    CURRENT_INSTANCE.update(author_id, name, last_name, email, birthdate)


@click.command()
def get_all_authors():
    CURRENT_INSTANCE.get_all()


@click.command()
def get_one_author(author_id, **kwargs):
    CURRENT_INSTANCE.get_one(
        author_id,
    )


@click.command()
def get_author_articles(author_id, **kwargs):
    CURRENT_INSTANCE.get_articles_by_author_id(author_id)
