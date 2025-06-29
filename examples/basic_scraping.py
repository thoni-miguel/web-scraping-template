#!/usr/bin/env python3
"""
Basic Web Scraping Example

This example demonstrates how to use the WebScraper template for simple data extraction.
"""

import asyncio
import yaml
from scraper_template import WebScraper


async def basic_scraping_example():
    """Example of basic web scraping with standard selectors."""

    # Configuration for scraping a simple website
    config = {
        "url": "https://quotes.toscrape.com/",
        "selectors": {
            "quotes": "div.quote span.text",
            "authors": "div.quote small.author",
            "tags": "div.quote div.tags a.tag",
        },
        "output_format": "csv",
        "wait_time": 2000,
    }

    async with WebScraper(headless=True) as scraper:
        print("Starting basic scraping example...")

        # Extract data
        data = await scraper.extract(config)

        # Save data
        await scraper.save_data(data, "quotes_data.csv", "csv")

        # Take screenshot for debugging
        await scraper.take_screenshot("quotes_screenshot.png")

        print("Basic scraping completed successfully!")
        print(f"Data shape: {data.shape if hasattr(data, 'shape') else 'N/A'}")


if __name__ == "__main__":
    asyncio.run(basic_scraping_example())
