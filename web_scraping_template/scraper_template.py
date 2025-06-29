import asyncio
import time
import yaml
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from playwright.async_api import async_playwright, Browser, Page
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """
    Configurable web scraper using Playwright with support for custom extraction functions.
    Designed for Fiverr gigs and reusable across different client requirements.
    """

    def __init__(self, headless: bool = True, slow_mo: int = 100):
        """
        Initialize the web scraper.

        Args:
            headless: Run browser in headless mode
            slow_mo: Delay between actions in milliseconds
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop()

    async def start(self):
        """Start the browser and create a new page."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless, slow_mo=self.slow_mo
        )
        self.page = await self.browser.new_page()
        logger.info("Browser started successfully")

    async def stop(self):
        """Stop the browser and cleanup."""
        if self.browser:
            await self.browser.close()
        if hasattr(self, "playwright"):
            await self.playwright.stop()
        logger.info("Browser stopped successfully")

    async def extract(self, config: Dict[str, Any]) -> Any:
        """
        Main extraction method that supports both standard and custom extraction.

        Args:
            config: Configuration dictionary containing extraction parameters

        Returns:
            Extracted data in the specified format
        """
        try:
            if "custom_function" in config:
                logger.info("Using custom extraction function")
                return await config["custom_function"](self, config)
            else:
                logger.info("Using standard extraction method")
                return await self._standard_extract(config)
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            raise

    async def _standard_extract(self, config: Dict[str, Any]) -> Any:
        """
        Standard extraction method using CSS selectors.

        Args:
            config: Configuration dictionary

        Returns:
            Extracted data
        """
        url = config["url"]
        selectors = config.get("selectors", {})
        wait_time = config.get("wait_time", 2000)

        logger.info(f"Navigating to {url}")
        await self.page.goto(url, wait_until="networkidle")
        await self.page.wait_for_timeout(wait_time)

        # Handle infinite scroll if specified
        if config.get("infinite_scroll"):
            await self._handle_infinite_scroll(config)

        # Extract data using selectors
        data = {}
        for key, selector in selectors.items():
            try:
                elements = await self.page.query_selector_all(selector)
                if len(elements) == 1:
                    value = await elements[0].text_content()
                    data[key] = value.strip() if value else ""
                else:
                    values = []
                    for element in elements:
                        value = await element.text_content()
                        if value:
                            values.append(value.strip())
                    data[key] = values
            except Exception as e:
                logger.warning(
                    f"Failed to extract {key} with selector {selector}: {str(e)}"
                )
                data[key] = ""

        # Handle multiple pages if specified
        if config.get("multi_page"):
            data = await self._handle_multi_page(config, data)

        return self._format_output(data, config.get("output_format", "json"))

    async def _handle_infinite_scroll(self, config: Dict[str, Any]):
        """Handle infinite scroll scenarios."""
        max_scrolls = config.get("max_scrolls", 10)
        scroll_delay = config.get("scroll_delay", 2000)

        for i in range(max_scrolls):
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await self.page.wait_for_timeout(scroll_delay)
            logger.info(f"Scroll {i+1}/{max_scrolls} completed")

    async def _handle_multi_page(
        self, config: Dict[str, Any], initial_data: Dict
    ) -> Dict:
        """Handle multi-page extraction scenarios."""
        pagination_selector = config.get("pagination_selector")
        max_pages = config.get("max_pages", 5)

        all_data = [initial_data] if initial_data else []

        for page_num in range(2, max_pages + 1):
            try:
                # Click next page button
                next_button = await self.page.query_selector(pagination_selector)
                if not next_button:
                    break

                await next_button.click()
                await self.page.wait_for_timeout(2000)

                # Extract data from current page
                page_data = await self._extract_page_data(config)
                all_data.append(page_data)

            except Exception as e:
                logger.warning(f"Failed to navigate to page {page_num}: {str(e)}")
                break

        return all_data

    async def _extract_page_data(self, config: Dict[str, Any]) -> Dict:
        """Extract data from current page."""
        selectors = config.get("selectors", {})
        data = {}

        for key, selector in selectors.items():
            try:
                elements = await self.page.query_selector_all(selector)
                values = []
                for element in elements:
                    value = await element.text_content()
                    if value:
                        values.append(value.strip())
                data[key] = values
            except Exception as e:
                logger.warning(f"Failed to extract {key}: {str(e)}")
                data[key] = []

        return data

    def _format_output(self, data: Any, output_format: str) -> Any:
        """
        Format output data according to specified format.

        Args:
            data: Raw extracted data
            output_format: Desired output format (json, csv, excel)

        Returns:
            Formatted data
        """
        if output_format.lower() == "json":
            return data
        elif output_format.lower() == "csv":
            if isinstance(data, list):
                return pd.DataFrame(data)
            else:
                return pd.DataFrame([data])
        elif output_format.lower() == "excel":
            if isinstance(data, list):
                return pd.DataFrame(data)
            else:
                return pd.DataFrame([data])
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    async def save_data(self, data: Any, filename: str, output_format: str):
        """
        Save extracted data to file.

        Args:
            data: Extracted data
            filename: Output filename
            output_format: File format
        """
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        filepath = output_dir / filename

        if output_format.lower() == "json":
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif output_format.lower() == "csv":
            if isinstance(data, pd.DataFrame):
                data.to_csv(filepath, index=False, encoding="utf-8")
            else:
                pd.DataFrame(data).to_csv(filepath, index=False, encoding="utf-8")
        elif output_format.lower() == "excel":
            if isinstance(data, pd.DataFrame):
                data.to_excel(filepath, index=False)
            else:
                pd.DataFrame(data).to_excel(filepath, index=False)

        logger.info(f"Data saved to {filepath}")

    async def take_screenshot(self, filename: str = "screenshot.png"):
        """Take a screenshot for debugging purposes."""
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        filepath = output_dir / filename
        await self.page.screenshot(path=str(filepath))
        logger.info(f"Screenshot saved to {filepath}")


# Example custom extraction functions
async def infinite_scroll_extract(scraper: WebScraper, config: Dict[str, Any]) -> Any:
    """
    Custom extraction function for infinite scroll scenarios.

    Args:
        scraper: WebScraper instance
        config: Configuration dictionary

    Returns:
        Extracted data
    """
    url = config["url"]
    item_selector = config.get("item_selector", "div.item")

    await scraper.page.goto(url, wait_until="networkidle")

    # Scroll to load more content
    max_scrolls = config.get("max_scrolls", 10)
    scroll_delay = config.get("scroll_delay", 2000)

    for i in range(max_scrolls):
        await scraper.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await scraper.page.wait_for_timeout(scroll_delay)

    # Extract all items
    items = await scraper.page.query_selector_all(item_selector)
    data = []

    for item in items:
        item_data = {}
        for key, selector in config.get("item_selectors", {}).items():
            try:
                element = await item.query_selector(selector)
                if element:
                    value = await element.text_content()
                    item_data[key] = value.strip() if value else ""
                else:
                    item_data[key] = ""
            except Exception as e:
                logger.warning(f"Failed to extract {key}: {str(e)}")
                item_data[key] = ""
        data.append(item_data)

    return scraper._format_output(data, config.get("output_format", "json"))


async def login_extract(scraper: WebScraper, config: Dict[str, Any]) -> Any:
    """
    Custom extraction function for sites requiring login.

    Args:
        scraper: WebScraper instance
        config: Configuration dictionary

    Returns:
        Extracted data
    """
    url = config["url"]
    login_config = config.get("login", {})

    await scraper.page.goto(url, wait_until="networkidle")

    # Handle login if credentials provided
    if login_config:
        username = login_config.get("username")
        password = login_config.get("password")
        username_selector = login_config.get("username_selector")
        password_selector = login_config.get("password_selector")
        submit_selector = login_config.get("submit_selector")

        if username and password:
            await scraper.page.fill(username_selector, username)
            await scraper.page.fill(password_selector, password)
            await scraper.page.click(submit_selector)
            await scraper.page.wait_for_timeout(3000)

    # Continue with standard extraction
    return await scraper._standard_extract(config)


# Main execution function
async def main():
    """Example usage of the WebScraper."""
    # Load configuration
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    async with WebScraper(headless=True) as scraper:
        # Extract data
        data = await scraper.extract(config)

        # Save data
        output_format = config.get("output_format", "json")
        filename = f"extracted_data.{output_format}"
        await scraper.save_data(data, filename, output_format)

        # Take screenshot for debugging
        await scraper.take_screenshot()


if __name__ == "__main__":
    asyncio.run(main())
