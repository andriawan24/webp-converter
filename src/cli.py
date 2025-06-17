import typer
from typing import Optional
from pathlib import Path
from src import __app_name__, __version__
from src.image import convert_image

app = typer.Typer(
    help=f"Welcome to {__app_name__} - Convert images to WebP format with ease!",
    epilog="Made with 🤍 by Fawwaz"
)

def _show_version(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

def _validate_quality(value: int) -> int:
    """Validate quality parameter is within valid range."""
    if not 1 <= value <= 100:
        raise typer.BadParameter("Quality must be between 1 and 100")
    return value

def _validate_file_path(value: str) -> str:
    """Validate that the source file exists."""
    path = Path(value)
    if not path.exists():
        raise typer.BadParameter(f"Source file does not exist: {value}")
    if not path.is_file():
        raise typer.BadParameter(f"Source path is not a file: {value}")
    return value

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
        help="Show the application's version and exit",
        callback=_show_version,
        is_eager=True
    )
) -> None:
    """WebP Converter CLI - Convert your images to WebP format efficiently."""
    return

@app.command(name="convert")
def convert(
    file_path: str = typer.Option(
        ...,
        "--source",
        "-s",
        help="Path to the source image file to convert",
        callback=_validate_file_path
    ),
    output_dir: str = typer.Option(
        ...,
        "--output-dir",
        "-o",
        help="Directory where the converted WebP file will be saved"
    ),
    quality: int = typer.Option(
        80,
        "--quality",
        "-q",
        help="Quality level for lossy compression (1-100, ignored for PNG)",
        callback=_validate_quality
    )
) -> None:
    """Convert an image file to WebP format.
    
    Supports PNG, JPEG, and MPO formats. PNG files are converted losslessly,
    while other formats use the specified quality setting.
    
    Example: webp-converter convert -s image.jpg -o ./output -q 85
    """
    try:
        output_path = Path(output_dir)
        if output_path.exists() and not output_path.is_dir():
            typer.echo(f"❌ Error: Output path exists but is not a directory: {output_dir}", err=True)
            raise typer.Exit(code=1)
        
        result_path = convert_image(file_path, output_dir, quality=quality)
        source_name = Path(file_path).name

        typer.echo(f"✅ Successfully converted '{source_name}' to WebP")
        typer.echo(f"📁 Output saved to: {result_path}")
    except FileNotFoundError as e:
        typer.echo(f"❌ File not found: {e}", err=True)
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(f"❌ {e}", err=True)
        raise typer.Exit(code=1)
    except PermissionError as e:
        typer.echo(f"❌ Permission denied: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error occurred: {e}", err=True)
        typer.echo("Please check your input and try again.", err=True)
        raise typer.Exit(code=1)