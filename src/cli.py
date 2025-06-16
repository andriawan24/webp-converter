import typer
from typing import Optional
from src import __app_name__, __version__

app = typer.Typer(help=f"Welcome to {__app_name__}, you can convert your image easily through command line")

def _show_version(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback(epilog="Made with 🤍 by Fawwaz")
def main(
    version: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
        help="Show the application's version",
        callback=_show_version,
        is_eager=True
    )
) -> None:
    return

@app.command(epilog="Hello")
def hello(name: str):
    print(f"Hello, {name}!")

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye, {name}. Have a good day!")
    else:
        print(f"Bye-bye swoosh swoosh {name}!")