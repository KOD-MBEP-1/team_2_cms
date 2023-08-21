import click
from author_cli import author
from categories_cli import category
from articles_cli import article


@click.group()
def cli():
    pass


cli.add_command(author)
cli.add_command(category)
cli.add_command(article)


if __name__ == "__main__":
    cli()
