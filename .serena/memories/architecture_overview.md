# Architecture Overview

## Core Components

### GeminiConversationParser (gemini_parser.py)
- **Purpose**: Extracts conversation data from Gemini HTML exports
- **Key Methods**:
  - `parse_html_file()`: Reads and parses HTML file
  - `parse_html_content()`: Processes HTML content to extract user-query and model-response pairs
  - `_extract_text_content()`: Helper method for clean text extraction
- **Storage**: Maintains conversations list internally

### MarkdownFormatter (markdown_formatter.py)
- **Purpose**: Converts parsed conversations to Markdown format
- **Key Methods**:
  - `format_conversations()`: Main formatting method with title support
  - `format_simple()`: Basic formatting without title
  - `save_to_file()`: File output with UTF-8 encoding
- **Output**: Clean Markdown with proper headings and separators

### Main CLI Interface (main.py)
- **Single File Processing**: `process_single_file()`
- **Batch Processing**: `process_batch()` with glob pattern support
- **CLI Arguments**: Uses argparse for input/output specification and batch options
- **Error Handling**: Comprehensive error handling with exit codes