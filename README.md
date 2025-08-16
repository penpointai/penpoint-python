# Penpoint Python Client

Official Python client library for the Penpoint API. This library provides a simple and intuitive interface for interacting with Penpoint's document processing and reference search capabilities.

## Features

- **File Management**: Upload, list, update, and delete files
- **Discrete References**: Search documents with three levels of precision (Basic, Standard, Advanced)
- **File Markup**: Generate marked-up versions of documents with highlighted references
- **Type Safety**: Full type hints and modern Python support
- **Async Support**: Both synchronous and asynchronous client interfaces

## Installation

```bash
pip install penpoint
```

## Quick Start

```python
from penpoint import PenpointClient

# Initialize the client with your API key
client = PenpointClient(api_key="your_api_key_here")

# Upload a file
with open("document.pdf", "rb") as f:
    file_obj = client.files.upload(
        file=f,
        filename="document.pdf",
        summary="A sample document for testing"
    )

# Search for references
references = client.discrete_references.basic(
    file_id=file_obj.id,
    prompt="CMake integration",
    markup_file=True,
    markup_color="#362580"
)

print(f"Found {len(references.parts)} references")
```

## API Reference

### Authentication

All API requests require an API key, which should be passed as the `x-api-key` header.

### Files

#### List Files
```python
files = client.files.list(limit=20, offset=0)
```

#### Upload File
```python
file_obj = client.files.upload(
    file=file_handle,
    filename="document.pdf",
    summary="Document description"
)
```

#### Update File
```python
updated_file = client.files.update(
    file_id=123,
    summary="Updated description",
    expiration_date="2025-12-31"
)
```

#### Delete File
```python
client.files.delete(file_id=123)
```

### Discrete References

#### Basic Search
```python
references = client.discrete_references.basic(
    file_id=123,
    prompt="search term",
    markup_file=True,
    markup_color="#FF0000"
)
```

#### Standard Search
```python
references = client.discrete_references.standard(
    file_id=123,
    prompt="search term",
    markup_file=True,
    markup_color="#FF0000"
)
```

#### Advanced Search
```python
references = client.discrete_references.advanced(
    file_id=123,
    prompt="search term",
    markup_file=True,
    markup_color="#FF0000"
)
```

## Configuration

The client can be configured with various options:

```python
from penpoint import PenpointClient

client = PenpointClient(
    api_key="your_api_key",
    base_url="https://api.penpoint.ai/v1",  # Default
    timeout=30,  # Request timeout in seconds
    max_retries=3  # Maximum retry attempts
)
```

## Error Handling

The library provides comprehensive error handling:

```python
from penpoint import PenpointError, PenpointAPIError

try:
    files = client.files.list()
except PenpointAPIError as e:
    print(f"API Error: {e.status_code} - {e.message}")
except PenpointError as e:
    print(f"Client Error: {e}")
```

## Async Support

For asynchronous applications, use the async client:

```python
from penpoint import AsyncPenpointClient
import asyncio

async def main():
    client = AsyncPenpointClient(api_key="your_api_key")
    
    files = await client.files.list()
    print(f"Found {len(files.data)} files")

asyncio.run(main())
```

## Development

### Setup

```bash
git clone https://github.com/penpoint/penpoint-python.git
cd penpoint-python
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black penpoint/
flake8 penpoint/
mypy penpoint/
```

### Publishing
```bash
cd python
make build          # Build the package
make publish        # Publish to PyPI (requires twine setup)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [https://penpoint-python.readthedocs.io/](https://penpoint-python.readthedocs.io/)
- Issues: [https://github.com/penpoint/penpoint-python/issues](https://github.com/penpoint/penpoint-python/issues)
- API Reference: [https://api.penpoint.ai/docs](https://api.penpoint.ai/docs)
