import typer
from typing import Optional, List
from pathlib import Path
from src import __app_name__, __version__
from src.image import convert_image
import glob

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

def _get_image_files(sources: List[str]) -> List[Path]:
    """Get all valid image files from the provided sources (files, directories, or patterns)."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.mpo'}
    files = []
    
    for source in sources:
        source_path = Path(source)
        
        if source_path.is_file():
            if source_path.suffix.lower() in image_extensions:
                files.append(source_path)
        elif source_path.is_dir():
            for ext in image_extensions:
                files.extend(source_path.rglob(f"*{ext}"))
        else:
            glob_files = glob.glob(source, recursive=True)
            for file_path in glob_files:
                path = Path(file_path)
                if path.is_file() and path.suffix.lower() in image_extensions:
                    files.append(path)
    
    return list(set(files))

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

@app.command(name="convert-batch")
def convert_batch(
    sources: List[str] = typer.Option(
        ...,
        "--source",
        "-s",
        help="Source files, directories, or glob patterns to convert (can be specified multiple times)"
    ),
    output_dir: str = typer.Option(
        ...,
        "--output-dir",
        "-o",
        help="Directory where the converted WebP files will be saved"
    ),
    quality: int = typer.Option(
        80,
        "--quality",
        "-q",
        help="Quality level for lossy compression (1-100, ignored for PNG)",
        callback=_validate_quality
    ),
    continue_on_error: bool = typer.Option(
        True,
        "--continue-on-error/--stop-on-error",
        help="Continue processing other files if one fails"
    )
) -> None:
    """Convert multiple image files to WebP format.
    
    Supports PNG, JPEG, and MPO formats. You can specify:
    - Individual files: -s image1.jpg -s image2.png
    - Directories: -s ./photos (processes all images recursively)
    - Glob patterns: -s "*.jpg" -s "photos/**/*.png"
    
    PNG files are converted losslessly, while other formats use the specified quality setting.
    
    Examples:
      webp-converter convert-batch -s photo1.jpg -s photo2.png -o ./output
      webp-converter convert-batch -s ./photos -o ./webp_output -q 90
      webp-converter convert-batch -s "*.jpg" -s "**/*.png" -o ./converted
    """
    try:
        output_path = Path(output_dir)
        if output_path.exists() and not output_path.is_dir():
            typer.echo(f"❌ Error: Output path exists but is not a directory: {output_dir}", err=True)
            raise typer.Exit(code=1)
        
        image_files = _get_image_files(sources)
        
        if not image_files:
            typer.echo("❌ No valid image files found in the specified sources", err=True)
            typer.echo("Supported formats: PNG, JPEG, MPO", err=True)
            raise typer.Exit(code=1)
        
        typer.echo(f"🔍 Found {len(image_files)} image file(s) to convert")
        
        successful_conversions = 0
        failed_conversions = 0
        failed_files = []
        
        for i, file_path in enumerate(image_files, 1):
            try:
                typer.echo(f"[{i}/{len(image_files)}] Converting {file_path.name}...", nl=False)
                _ = convert_image(str(file_path), output_dir, quality=quality)
                typer.echo(f" ✅")
                successful_conversions += 1
                
            except Exception as e:
                typer.echo(f" ❌ Failed: {e}")
                failed_conversions += 1
                failed_files.append((file_path.name, str(e)))
                
                if not continue_on_error:
                    typer.echo(f"❌ Stopping due to error (use --continue-on-error to skip failed files)", err=True)
                    raise typer.Exit(code=1)
        
        # Summary
        typer.echo("\n" + "="*50)
        typer.echo(f"📊 Conversion Summary:")
        typer.echo(f"   ✅ Successful: {successful_conversions}")
        typer.echo(f"   ❌ Failed: {failed_conversions}")
        typer.echo(f"   📁 Output directory: {output_dir}")
        
        if failed_files:
            typer.echo(f"\n❌ Failed files:")
            for filename, error in failed_files:
                typer.echo(f"   • {filename}: {error}")
        
        if failed_conversions > 0 and not continue_on_error:
            raise typer.Exit(code=1)
    except KeyboardInterrupt:
        typer.echo(f"\n❌ Operation cancelled by user", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error occurred: {e}", err=True)
        raise typer.Exit(code=1)