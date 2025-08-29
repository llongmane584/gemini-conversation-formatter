# Code Style and Conventions

## General Style
- Uses Japanese comments and docstrings throughout the codebase
- Type hints are used for method parameters and return types
- Classes follow PascalCase naming (GeminiConversationParser, MarkdownFormatter)
- Methods follow snake_case naming
- Private methods prefixed with underscore (_extract_text_content)

## Code Organization
- Clean separation of concerns: parsing logic separate from formatting logic
- Classes are focused and single-responsibility
- Functions have descriptive docstrings in Japanese
- Error handling with try/catch blocks and appropriate exit codes

## File Structure Pattern
- Each major functionality in separate module (parser, formatter)
- Main entry point handles CLI arguments and orchestration
- Clear separation between single file and batch processing logic