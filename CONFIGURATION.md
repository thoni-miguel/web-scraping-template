# Configuration Reference

This document provides a complete reference for all configuration options available in the Web Scraping Template library.

## Configuration Structure

The library accepts configuration in two formats:
- **Python Dictionary** (recommended for scripts)
- **YAML File** (recommended for complex setups)

## Basic Configuration

### Required Settings

| Setting | Type | Description | Example |
|---------|------|-------------|---------|
| `url` | string | Target website URL | `"https://example.com"` |
| `selectors` | dict | CSS selectors for data extraction | `{"title": "h1"}` |

### Optional Settings

| Setting | Type | Default | Description | Example |
|---------|------|---------|-------------|---------|
| `output_format` | string | `"json"` | Output file format | `"csv"`, `"excel"` |
| `wait_time` | integer | `2000` | Milliseconds to wait after page load | `5000` |
| `headless` | boolean | `true` | Run browser in headless mode | `false` |
| `slow_mo` | integer | `100` | Delay between actions (ms) | `500` |

## Browser Settings

### `headless`
Controls whether the browser runs in visible or hidden mode.

**Values:**
- `true` - Browser runs in background (faster, no visual)
- `false` - Browser window is visible (good for debugging)

**Example:**
```python
config = {
    'url': 'https://example.com',
    'headless': False,  # See the browser in action
    'selectors': {'title': 'h1'}
}
```

### `slow_mo`
Adds delay between browser actions for debugging or rate limiting.

**Values:**
- `0` - No delay (fastest)
- `100-1000` - Small delay (good for debugging)
- `1000+` - Longer delay (rate limiting)

**Example:**
```python
config = {
    'url': 'https://example.com',
    'slow_mo': 500,  # 500ms between actions
    'selectors': {'title': 'h1'}
}
```

## Data Extraction Settings

### `selectors`
CSS selectors for extracting data from the page.

**Format:** `{"key": "css_selector"}`

**Example:**
```python
config = {
    'url': 'https://example.com',
    'selectors': {
        'title': 'h1.product-title',
        'price': 'span.price',
        'description': 'div.product-description',
        'images': 'img.product-image'
    }
}
```

**Behavior:**
- **Single element found**: Returns string value
- **Multiple elements found**: Returns list of values
- **No elements found**: Returns empty string/list

### `custom_function`
Use custom extraction logic instead of CSS selectors.

**Values:**
- Function object
- Built-in functions: `infinite_scroll_extract`, `login_extract`

**Example:**
```python
from web_scraping_template import infinite_scroll_extract

config = {
    'url': 'https://example.com',
    'custom_function': infinite_scroll_extract,
    'item_selector': 'div.item',
    'item_selectors': {
        'title': 'h3.title',
        'price': 'span.price'
    }
}
```

## Output Format Settings

### `output_format`
Specifies the format for saved data.

**Values:**
- `"json"` - Structured JSON format
- `"csv"` - Comma-separated values (spreadsheet)
- `"excel"` - Excel file with formatting

**Example:**
```python
config = {
    'url': 'https://example.com',
    'selectors': {'title': 'h1'},
    'output_format': 'csv'  # Save as CSV file
}
```

## Infinite Scroll Settings

### `infinite_scroll`
Enable infinite scroll handling (requires custom function).

**Values:**
- `true` - Enable infinite scroll
- `false` - Disable (default)

### `max_scrolls`
Maximum number of scroll operations.

**Values:**
- `1-50` - Reasonable range
- `10` - Good default

### `scroll_delay`
Delay between scroll operations (milliseconds).

**Values:**
- `1000-5000` - Recommended range
- `2000` - Good default

**Example:**
```python
config = {
    'url': 'https://example.com',
    'custom_function': infinite_scroll_extract,
    'infinite_scroll': True,
    'max_scrolls': 15,
    'scroll_delay': 3000
}
```

## Multi-Page Settings

### `multi_page`
Enable pagination handling.

**Values:**
- `true` - Enable multi-page extraction
- `false` - Disable (default)

### `pagination_selector`
CSS selector for the "next page" button.

**Example:**
```python
config = {
    'url': 'https://example.com',
    'selectors': {'title': 'h1'},
    'multi_page': True,
    'pagination_selector': 'a.next-page',
    'max_pages': 5
}
```

### `max_pages`
Maximum number of pages to scrape.

**Values:**
- `1-100` - Reasonable range
- `5` - Good default

## Login Settings

### `login`
Authentication configuration (requires custom function).

**Structure:**
```python
login = {
    'username': 'your_username',
    'password': 'your_password',
    'username_selector': '#username',
    'password_selector': '#password',
    'submit_selector': 'button[type="submit"]'
}
```

**Example:**
```python
from web_scraping_template import login_extract

config = {
    'url': 'https://example.com',
    'custom_function': login_extract,
    'login': {
        'username': 'myuser@example.com',
        'password': 'mypassword123',
        'username_selector': '#email',
        'password_selector': '#password',
        'submit_selector': 'button[type="submit"]'
    }
}
```

## Item-Specific Settings (for Infinite Scroll)

### `item_selector`
CSS selector for individual items in a list.

**Example:**
```python
config = {
    'url': 'https://example.com',
    'custom_function': infinite_scroll_extract,
    'item_selector': 'div.product-item',
    'item_selectors': {
        'title': 'h3.title',
        'price': 'span.price'
    }
}
```

### `item_selectors`
CSS selectors for data within each item.

**Format:** `{"key": "css_selector"}`

## Rate Limiting Settings

### `rate_limit`
Rate limiting configuration.

**Structure:**
```python
rate_limit = {
    'requests_per_minute': 60,
    'delay_between_requests': 1000
}
```

**Example:**
```python
config = {
    'url': 'https://example.com',
    'selectors': {'title': 'h1'},
    'rate_limit': {
        'requests_per_minute': 30,  # Conservative rate
        'delay_between_requests': 2000  # 2 seconds between requests
    }
}
```

## Screenshot Settings

### `take_screenshot`
Enable automatic screenshot capture.

**Values:**
- `true` - Take screenshots
- `false` - Disable (default)

### `screenshot_filename`
Custom filename for screenshots.

**Example:**
```python
config = {
    'url': 'https://example.com',
    'selectors': {'title': 'h1'},
    'take_screenshot': True,
    'screenshot_filename': 'debug_screenshot.png'
}
```

## Complete Configuration Example

```python
config = {
    # Basic settings
    'url': 'https://example.com',
    'output_format': 'csv',
    'wait_time': 3000,
    
    # Browser settings
    'headless': False,
    'slow_mo': 500,
    
    # Data extraction
    'selectors': {
        'title': 'h1.product-title',
        'price': 'span.price',
        'description': 'div.description'
    },
    
    # Advanced features
    'multi_page': True,
    'pagination_selector': 'a.next',
    'max_pages': 10,
    
    # Rate limiting
    'rate_limit': {
        'requests_per_minute': 30,
        'delay_between_requests': 2000
    },
    
    # Debugging
    'take_screenshot': True,
    'screenshot_filename': 'debug.png'
}
```

## YAML Configuration Example

```yaml
# Basic Configuration
url: "https://example.com"
output_format: "csv"
wait_time: 3000

# Browser Settings
headless: false
slow_mo: 500

# Data Extraction
selectors:
  title: "h1.product-title"
  price: "span.price"
  description: "div.description"

# Advanced Features
multi_page: true
pagination_selector: "a.next"
max_pages: 10

# Rate Limiting
rate_limit:
  requests_per_minute: 30
  delay_between_requests: 2000

# Debugging
take_screenshot: true
screenshot_filename: "debug.png"
```
