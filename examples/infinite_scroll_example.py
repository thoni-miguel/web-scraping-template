#!/usr/bin/env python3
"""
Infinite Scroll Scraping Example

This example demonstrates how to use custom extraction functions for infinite scroll scenarios.
"""

import asyncio
import sys
import os

# Add parent directory to path to import scraper_template
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper_template import WebScraper, infinite_scroll_extract


async def infinite_scroll_example():
    """Example of infinite scroll scraping using custom function."""

    # Configuration for infinite scroll scraping
    config = {
        "url": "https://quotes.toscrape.com/scroll",
        "custom_function": infinite_scroll_extract,
        "item_selector": "div.quote",
        "item_selectors": {
            "quote": "span.text",
            "author": "small.author",
            "tags": "div.tags a.tag",
        },
        "max_scrolls": 5,
        "scroll_delay": 2000,
        "output_format": "csv",
    }

    async with WebScraper(headless=True) as scraper:
        print("Starting infinite scroll scraping example...")

        try:
            # Extract data using custom function
            data = await scraper.extract(config)

            # Save data
            await scraper.save_data(data, "infinite_scroll_data.csv", "csv")

            # Take screenshot for debugging
            await scraper.take_screenshot("infinite_scroll_screenshot.png")

            print("Infinite scroll scraping completed successfully!")
            print(f"Extracted {len(data)} items")

        except Exception as e:
            print(f"Error during infinite scroll scraping: {str(e)}")
            # Take screenshot for debugging
            await scraper.take_screenshot("error_screenshot.png")


if __name__ == "__main__":
    asyncio.run(infinite_scroll_example())
