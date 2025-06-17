from PIL import Image
from pathlib import Path

SUPPORTED_FORMATS = {"PNG", "JPEG", "MPO"}

def get_image(file_path: str) -> Image:
    """ Open and validate image file"""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {file_path}")

    try:
        image = Image.open(file_path)

        if image.format not in SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {image.format}")
        
        return image
    except Exception as e:
        if isinstance(e, (FileNotFoundError, ValueError)):
            raise
        raise ValueError(f"Failed to open image: {e}")

def convert_image(file_path: str, output_dir: str, quality: int = 80):
    """ Convert an image to WEBP Format """
    image = get_image(file_path=file_path)

    input_path = Path(file_path)
    output_path = Path(output_dir)

    # Create the folder if needed
    output_path.mkdir(parents=True, exist_ok=True)

    final_path = output_path / f"{input_path.stem}.webp"

    save_kwargs = {"format": "webp"}
    if image.format == "PNG":
        save_kwargs["lossless"] = True
    else:
        save_kwargs["quality"] = quality

    try:
        image.save(final_path, **save_kwargs)
        return final_path
    finally:
        image.close()