import typer as typer

from .generator import (
    generate,
)

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
)


@app.command()
def main_command(uri: str):
    """
    Generates http client based on https library from OpenAPI json schema
    """
    generate(uri)


def main():
    app()
