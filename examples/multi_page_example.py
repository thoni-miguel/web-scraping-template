#!/usr/bin/env python3
"""
Multi-Page Scraping Example

This example demonstrates how to scrape data from multiple pages using pagination.
"""

import asyncio
import sys
import os

# Add parent directory to path to import scraper_template
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper_template import WebScraper


async def multi_page_example():
    """Example of multi-page scraping with pagination."""

    # Configuration for multi-page scraping
    config = {
        "url": "https://quotes.toscrape.com/",
        "selectors": {
            "quotes": "div.quote span.text",
            "authors": "div.quote small.author",
            "tags": "div.quote div.tags a.tag",
        },
        "multi_page": True,
        "pagination_selector": "li.next a",
        "max_pages": 3,
        "output_format": "csv",
        "wait_time": 2000,
    }

    async with WebScraper(headless=True) as scraper:
        print("Starting multi-page scraping example...")

        try:
            # Extract data from multiple pages
            data = await scraper.extract(config)

            # Save data
            await scraper.save_data(data, "multi_page_data.csv", "csv")

            # Take screenshot for debugging
            await scraper.take_screenshot("multi_page_screenshot.png")

            print("Multi-page scraping completed successfully!")
            print(f"Extracted data from {len(data)} pages")

        except Exception as e:
            print(f"Error during multi-page scraping: {str(e)}")
            # Take screenshot for debugging
            await scraper.take_screenshot("error_screenshot.png")


if __name__ == "__main__":
    asyncio.run(multi_page_example())
