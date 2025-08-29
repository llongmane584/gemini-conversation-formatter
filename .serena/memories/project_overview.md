# Project Overview

## Purpose
Gemini Conversation Formatter is a Python tool that converts Gemini AI conversation HTML files to structured Markdown format. It extracts user queries and model responses from exported Gemini conversation HTML files and formats them as readable Markdown documents.

## Tech Stack
- **Language**: Python 3.12+
- **Package Manager**: UV (ultra-fast Python package manager)
- **Dependencies**: BeautifulSoup4 for HTML parsing
- **Environment**: Uses .venv for virtual environment management

## Project Structure
- `main.py` - Entry point with CLI interface and batch processing
- `gemini_parser.py` - HTML parsing logic using BeautifulSoup4
- `markdown_formatter.py` - Markdown formatting and output generation
- `pyproject.toml` - Project configuration and dependencies
- `.python-version` - Python version specification (3.12)
- `examples/` - Sample HTML files (gitignored)