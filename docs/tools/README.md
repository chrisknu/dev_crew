# Tools Documentation

This document outlines the tools available in the DevCrew project and their usage.

## Tool Categories

### 1. Browser Tools

Tools for web interaction and scraping:

```python
class BrowserTools:
    @tool('Scrape website content')
    def scrape_and_summarize_website(website):
        '''Scrapes and summarizes website content'''
        pass
```

### 2. File Tools

Tools for file operations:

```python
class FileTools:
    @tool('Write file with content')
    def write_file(data):
        '''Writes content to a file'''
        pass
```

### 3. Search Tools

Tools for internet searches:

```python
class SearchTools:
    @tool('Search internet')
    def search_internet(query):
        '''Performs internet search'''
        pass
```

## Tool Integration

### Adding New Tools

1. Create a new tool class in `tools/` directory
2. Use the `@tool` decorator with description
3. Implement the tool interface
4. Add error handling
5. Register the tool with agents

Example:

```python
from crewai import Tool

class CustomTool:
    @tool('Custom tool description')
    def custom_action(self, input_data):
        '''Detailed description of the tool'''
        try:
            # Tool implementation
            pass
        except Exception as e:
            return f"Error: {str(e)}"
```

### Tool Configuration

Tools can be configured through:

1. Environment variables
2. Configuration files
3. Runtime parameters

## Best Practices

1. **Documentation**

   - Document tool purpose
   - Provide usage examples
   - List requirements

2. **Error Handling**

   - Implement proper error handling
   - Return meaningful error messages
   - Log errors appropriately

3. **Testing**
   - Write unit tests
   - Test edge cases
   - Mock external dependencies

## Available Tools

| Tool Name       | Description              | Required Config     |
| --------------- | ------------------------ | ------------------- |
| scrape_website  | Scrapes website content  | BROWSERLESS_API_KEY |
| search_internet | Performs internet search | SERPER_API_KEY      |
| write_file      | Writes content to file   | None                |

## Tool Usage Examples

### Web Scraping

```python
result = BrowserTools.scrape_and_summarize_website("https://example.com")
```

### File Operations

```python
FileTools.write_file("path/to/file|content to write")
```

### Internet Search

```python
results = SearchTools.search_internet("search query")
```
