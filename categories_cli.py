from Categories import Category
import click

CURRENT_INSTANCE = None


CATEGORY_ACTIONS = ["create", "get_all", "update", "get_one", "get_articles"]


@click.command()
@click.option(
    "--action",
    "-a",
    prompt="Select an action to perform on Author table",
    type=click.Choice(CATEGORY_ACTIONS),
    help="Select an action to perform on Author table",
)
@click.option(
    "--name",
    prompt=False,
    help="Type the name of your category",
)
@click.option(
    "--description",
    prompt=False,
    help="Type the description of your category",
)
@click.option(
    "--category_id",
    prompt=False,
    help="Type the category_id you want to refer to",
)
@click.pass_context
def category(ctx, action, **kwargs):
    global CURRENT_INSTANCE
    CURRENT_INSTANCE = Category()
    match action:
        case "create":
            ctx.invoke(create_category, **kwargs)
        case "update":
            ctx.invoke(update_category, **kwargs)
        case "get_one":
            ctx.invoke(get_one_category, **kwargs)
        case "get_articles":
            ctx.invoke(get_category_articles, **kwargs)
        case "get_all":
            ctx.invoke(get_all_categories)


@click.command()
def create_category(name, description, **kwargs):
    CURRENT_INSTANCE.create(
        name,
        description,
    )


@click.command()
def update_category(name, description, category_id, **kwargs):
    CURRENT_INSTANCE.update(
        category_id,
        name,
        description,
    )


@click.command()
def get_all_categories():
    CURRENT_INSTANCE.get_all()


@click.command()
def get_one_category(category_id, **kwargs):
    CURRENT_INSTANCE.get_one(
        category_id,
    )


@click.command()
def get_category_articles(category_id, **kwargs):
    CURRENT_INSTANCE.get_articles_by_category_id(category_id)
