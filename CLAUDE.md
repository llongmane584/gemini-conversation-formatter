# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Setup

IMPORTANT!!!!!

```bash
# Environment setup
uv venv
source .venv/bin/activate
uv add beautifulsoup4

# Run single file conversion
python main.py input.html [output.md]

# Run batch processing
python main.py "pattern/*.html" --batch --output-dir converted/
```

## Project Overview
Gemini Conversation Formatter converts Gemini AI conversation HTML exports to structured Markdown format. It parses HTML files to extract user queries and model responses, then formats them as readable Markdown documents.

## Tech Stack
- Python 3.12+ (specified in .python-version)
- UV package manager for dependency management
- BeautifulSoup4 for HTML parsing


## Architecture
The codebase follows a clean separation of concerns with three main components:

- **GeminiConversationParser** (`gemini_parser.py`): Handles HTML parsing and conversation extraction
- **MarkdownFormatter** (`markdown_formatter.py`): Converts parsed data to Markdown format  
- **Main CLI** (`main.py`): Provides command-line interface with single file and batch processing

## Code Conventions
- Japanese comments and docstrings throughout
- Type hints for method parameters and return types
- PascalCase for classes, snake_case for methods
- Private methods prefixed with underscore
- UTF-8 encoding for all file operations
- Comprehensive error handling with appropriate exit codes

## Key Commands
- Single conversion: `python main.py input.html [output.md]`
- Batch conversion: `python main.py "*.html" --batch --output-dir converted/`
- Environment activation: `source .venv/bin/activate`
