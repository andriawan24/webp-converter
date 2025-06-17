# WebP Converter

A powerful command-line tool for converting images to WebP format with ease! Convert single images or batch process multiple files with customizable quality settings.

## Features

- 🖼️ **Multiple Format Support**: Convert PNG, JPEG, and MPO images to WebP
- 🔧 **Quality Control**: Adjustable quality settings for lossy compression (1-100)
- 📁 **Batch Processing**: Convert multiple files, directories, or glob patterns
- 🔄 **Smart Conversion**: PNG files are converted losslessly, others use quality settings
- 💪 **Error Handling**: Robust error handling with continue-on-error options
- 🎯 **Easy to Use**: Simple CLI interface with helpful commands

## Installation

1. Clone the repository:
```bash
git clone https://github.com/andriawan24/webp-converter.git
cd webp-converter
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Convert a Single Image

Convert a single image file to WebP format:

```bash
python main.py convert -s input.jpg -o ./output -q 85
```

**Parameters:**
- `-s, --source`: Path to the source image file
- `-o, --output-dir`: Directory where the converted WebP file will be saved
- `-q, --quality`: Quality level for lossy compression (1-100, default: 80)

### Batch Convert Multiple Images

Convert multiple images at once:

```bash
# Convert specific files
python main.py convert-batch -s photo1.jpg -s photo2.png -o ./output

# Convert all images in a directory (recursive)
python main.py convert-batch -s ./photos -o ./webp_output -q 90

# Use glob patterns
python main.py convert-batch -s "*.jpg" -s "**/*.png" -o ./converted
```

**Parameters:**
- `-s, --source`: Source files, directories, or glob patterns (can be specified multiple times)
- `-o, --output-dir`: Directory where converted WebP files will be saved
- `-q, --quality`: Quality level for lossy compression (1-100, default: 80)
- `--continue-on-error/--stop-on-error`: Continue processing if one file fails (default: continue)

### Get Version Information

```bash
python main.py --version
```

## Supported Formats

- **PNG** → WebP (lossless conversion)
- **JPEG** → WebP (lossy conversion with quality setting)
- **MPO** → WebP (lossy conversion with quality setting)

## Examples

### Basic Usage
```bash
# Convert a single JPEG with default quality (80)
python main.py convert -s vacation.jpg -o ./webp_images

# Convert with high quality
python main.py convert -s portrait.jpg -o ./output -q 95

# Convert a PNG (automatically lossless)
python main.py convert -s logo.png -o ./assets
```

### Batch Processing
```bash
# Convert all JPEGs in current directory
python main.py convert-batch -s "*.jpg" -o ./converted

# Convert all images from multiple directories
python main.py convert-batch -s ./photos -s ./screenshots -o ./all_webp

# Process with custom quality and error handling
python main.py convert-batch -s ./images -o ./output -q 90 --stop-on-error
```

## Output

The tool provides clear feedback during conversion:

```
✅ Successfully converted 'vacation.jpg' to WebP
📁 Output saved to: ./output/vacation.webp

🔍 Found 5 image file(s) to convert
[1/5] Converting photo1.jpg... ✅
[2/5] Converting photo2.png... ✅
[3/5] Converting photo3.jpg... ✅
[4/5] Converting photo4.png... ✅
[5/5] Converting photo5.jpg... ✅

📊 Conversion Summary:
   ✅ Successfully converted: 5 files
   ❌ Failed conversions: 0 files
   📁 Output directory: ./output
```

## Error Handling

The tool includes comprehensive error handling for:
- File not found errors
- Invalid file formats
- Permission issues
- Invalid quality parameters
- Output directory problems

## Requirements

- Python 3.6+
- Pillow (PIL) for image processing
- Typer for CLI interface

## Development

To set up for development:

1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests (if available)

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Made with 🤍 by Fawwaz

## Version

Current version: 0.0.1
