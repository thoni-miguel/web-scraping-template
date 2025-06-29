# Web Scraping Template

I created this library because I was tired of writing the same web scraping boilerplate code over and over again. Every time I needed to scrape a different website, I found myself recreating the same patterns - browser setup, error handling, data extraction, and output formatting.

This library is my solution: a well-structured, documented, and ready-to-use foundation that lets me quickly build different scraping scripts without starting from scratch. Whether I'm working on Fiverr gigs or personal projects, I can now focus on the unique aspects of each scraping task rather than the repetitive setup.

## What This Library Gives You

- **Ready-to-use foundation**: No more boilerplate code - just import and use
- **Flexible architecture**: Handle simple selectors or complex custom logic
- **Built-in common scenarios**: Infinite scroll, multi-page extraction, login handling
- **Multiple output formats**: JSON, CSV, Excel - whatever your client needs
- **Robust error handling**: Screenshots, logging, and graceful failures
- **Async performance**: Built with modern Python async/await patterns
- **Professional packaging**: Installable via pip for easy reuse across projects

## Quick Start

### Installation

**Option 1: Install from local path (recommended for development)**
```bash
# Clone the repository
git clone <repository-url>
cd web-scraping-template

# Install the library in editable mode
pip install -e .

# Install Playwright browsers
playwright install
```

**Option 2: Use in a new project**
```bash
# In your new project directory
pip install -e /path/to/web-scraping-template
playwright install
```

### Basic Usage

```python
import asyncio
from web_scraping_template import WebScraper

async def main():
    config = {
        'url': 'https://quotes.toscrape.com/',
        'selectors': {
            'quotes': 'div.quote span.text',
            'authors': 'div.quote small.author',
            'tags': 'div.quote div.tags a.tag'
        },
        'output_format': 'csv'
    }
    
    async with WebScraper() as scraper:
        data = await scraper.extract(config)
        await scraper.save_data(data, 'quotes.csv', 'csv')
        await scraper.take_screenshot('debug.png')

asyncio.run(main())
```

### Using Custom Functions

```python
from web_scraping_template import WebScraper, infinite_scroll_extract

async def main():
    config = {
        'url': 'https://example.com',
        'custom_function': infinite_scroll_extract,
        'item_selector': 'div.item',
        'item_selectors': {
            'title': 'h3.title',
            'price': 'span.price'
        },
        'output_format': 'json'
    }
    
    async with WebScraper() as scraper:
        data = await scraper.extract(config)
        await scraper.save_data(data, 'data.json', 'json')

asyncio.run(main())
```

## How It Works

### The Core Concept

This library provides a `WebScraper` class that handles all the complex browser automation, while you focus on:

1. **Defining what to extract** (CSS selectors or custom logic)
2. **Configuring how to extract** (infinite scroll, pagination, etc.)
3. **Specifying output format** (JSON, CSV, Excel)

### Two Approaches

**Simple Approach**: Use CSS selectors for basic data extraction
```python
config = {
    'url': 'https://example.com',
    'selectors': {'title': 'h1', 'price': 'span.price'},
    'output_format': 'csv'
}
```

**Advanced Approach**: Use custom functions for complex scenarios
```python
config = {
    'url': 'https://example.com',
    'custom_function': my_custom_logic,
    'output_format': 'json'
}
```

## Built-in Features

### 1. Infinite Scroll Handling
```python
from web_scraping_template import infinite_scroll_extract

config = {
    'url': 'https://example.com',
    'custom_function': infinite_scroll_extract,
    'item_selector': 'div.item',
    'max_scrolls': 10,
    'scroll_delay': 2000
}
```

### 2. Multi-Page Extraction
```python
config = {
    'url': 'https://example.com',
    'selectors': {'title': 'h1'},
    'multi_page': True,
    'pagination_selector': 'a.next',
    'max_pages': 5
}
```

### 3. Login Handling
```python
from web_scraping_template import login_extract

config = {
    'url': 'https://example.com',
    'custom_function': login_extract,
    'login': {
        'username': 'your_username',
        'password': 'your_password',
        'username_selector': '#username',
        'password_selector': '#password',
        'submit_selector': 'button[type="submit"]'
    }
}
```

## Examples

The library includes comprehensive examples in the `examples/` directory:

- **Basic scraping**: Simple CSS selector extraction
- **Infinite scroll**: Handling dynamic content loading
- **Multi-page**: Pagination and navigation
- **Custom functions**: Specialized extraction logic

Run any example:
```bash
python examples/basic_scraping.py
```

## Configuration

For a complete reference of all configuration options, see [CONFIGURATION.md](CONFIGURATION.md).

The library supports both inline Python dictionaries and YAML files for configuration.

## Common Use Cases

### E-commerce Scraping
```python
config = {
    'url': 'https://shop.example.com',
    'selectors': {
        'product_name': 'h1.product-title',
        'price': 'span.price',
        'description': 'div.product-description',
        'images': 'img.product-image'
    },
    'output_format': 'csv'
}
```

### Social Media Scraping
```python
config = {
    'url': 'https://social.example.com/feed',
    'custom_function': infinite_scroll_extract,
    'item_selector': 'div.post',
    'item_selectors': {
        'content': 'div.post-content',
        'author': 'span.author',
        'timestamp': 'time.timestamp'
    },
    'max_scrolls': 20
}
```

### News/Content Scraping
```python
config = {
    'url': 'https://news.example.com',
    'selectors': {
        'headlines': 'h2.headline',
        'summaries': 'p.summary',
        'dates': 'span.date'
    },
    'multi_page': True,
    'pagination_selector': 'a.next-page',
    'output_format': 'json'
}
```

## Error Handling & Debugging

### Built-in Features
- **Screenshots**: Automatic capture on errors
- **Logging**: Detailed operation logs
- **Graceful failures**: Continues even if some elements fail
- **Retry logic**: Handles temporary network issues

### Debugging Tips
```python
# Enable visible browser for debugging
async with WebScraper(headless=False) as scraper:
    # Your scraping code here

# Take screenshots for debugging
await scraper.take_screenshot('debug.png')

# Increase delays for complex sites
config = {
    'wait_time': 5000,  # 5 seconds
    'slow_mo': 500      # 500ms between actions
}
```

## License

This project is licensed under the MIT License.

## Changelog

### Version 1.0.0
- Initial release with basic scraping functionality
- Support for custom extraction functions
- Multiple output formats (JSON, CSV, Excel)
- Infinite scroll and multi-page support
- Login handling capabilities
- Professional packaging for easy installation
