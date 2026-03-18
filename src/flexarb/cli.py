"""Command-line interface for flexarb."""

import typer

from flexarb import __version__

app = typer.Typer(
    name="flexarb",
    help="Calculating electricity price arbitrage across countries and times",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        typer.echo(f"flexarb version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Calculating electricity price arbitrage across countries and times."""


@app.command()
def hello(
    name: str = typer.Argument("World", help="Name to greet"),
) -> None:
    """Say hello to someone."""
    typer.echo(f"Hello, {name}!")


if __name__ == "__main__":
    app()
