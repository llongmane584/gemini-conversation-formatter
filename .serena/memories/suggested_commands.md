# Suggested Commands

## Environment Setup
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv add beautifulsoup4
```

## Running the Application
```bash
# Single file processing
python main.py input.html [output.md]

# Batch processing
python main.py "pattern/*.html" --batch
python main.py "pattern/*.html" --batch --output-dir converted/
```

## Development Commands
- No specific linting/testing commands found in project configuration
- Uses UV for dependency management
- Standard Python development workflow applies