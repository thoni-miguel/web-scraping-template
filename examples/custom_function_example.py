#!/usr/bin/env python3
"""
Custom Function Example

This example demonstrates how to create and use custom extraction functions
for specialized scraping scenarios.
"""

import asyncio
import sys
import os

# Add parent directory to path to import scraper_template
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper_template import WebScraper


async def custom_ecommerce_extract(scraper, config):
    """
    Custom extraction function for e-commerce product pages.

    This function demonstrates how to create specialized extraction logic
    for specific website types.
    """
    url = config["url"]

    await scraper.page.goto(url, wait_until="networkidle")
    await scraper.page.wait_for_timeout(2000)

    # Extract product information
    product_data = {}

    # Product title
    try:
        title_element = await scraper.page.query_selector("h1.product-title")
        if title_element:
            product_data["title"] = await title_element.text_content()
    except Exception as e:
        product_data["title"] = ""

    # Product price
    try:
        price_element = await scraper.page.query_selector("span.price")
        if price_element:
            product_data["price"] = await price_element.text_content()
    except Exception as e:
        product_data["price"] = ""

    # Product description
    try:
        desc_element = await scraper.page.query_selector("div.description")
        if desc_element:
            product_data["description"] = await desc_element.text_content()
    except Exception as e:
        product_data["description"] = ""

    # Product images
    try:
        image_elements = await scraper.page.query_selector_all("img.product-image")
        images = []
        for img in image_elements:
            src = await img.get_attribute("src")
            if src:
                images.append(src)
        product_data["images"] = images
    except Exception as e:
        product_data["images"] = []

    # Product reviews
    try:
        review_elements = await scraper.page.query_selector_all("div.review")
        reviews = []
        for review in review_elements:
            review_text = await review.text_content()
            if review_text:
                reviews.append(review_text.strip())
        product_data["reviews"] = reviews
    except Exception as e:
        product_data["reviews"] = []

    return scraper._format_output(product_data, config.get("output_format", "json"))


async def custom_function_example():
    """Example of using custom extraction functions."""

    # Configuration using custom function
    config = {
        "url": "https://example-ecommerce.com/product/123",
        "custom_function": custom_ecommerce_extract,
        "output_format": "json",
    }

    async with WebScraper(headless=True) as scraper:
        print("Starting custom function example...")

        try:
            # Extract data using custom function
            data = await scraper.extract(config)

            # Save data
            await scraper.save_data(data, "custom_function_data.json", "json")

            # Take screenshot for debugging
            await scraper.take_screenshot("custom_function_screenshot.png")

            print("Custom function scraping completed successfully!")
            print(f"Extracted data: {data}")

        except Exception as e:
            print(f"Error during custom function scraping: {str(e)}")
            # Take screenshot for debugging
            await scraper.take_screenshot("error_screenshot.png")


if __name__ == "__main__":
    asyncio.run(custom_function_example())
