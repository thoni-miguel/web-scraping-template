#!/usr/bin/env python3
"""
Installation script for Web Scraping Template
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main installation function."""
    print("Web Scraping Template Installation")
    print("=" * 40)

    # Check if Python 3.7+ is available
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher is required")
        sys.exit(1)

    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

    # Install the package in editable mode
    if not run_command("pip install -e .", "Installing web-scraping-template package"):
        print("Failed to install the package. Please check your Python environment.")
        sys.exit(1)

    # Install Playwright browsers
    if not run_command("playwright install", "Installing Playwright browsers"):
        print("Failed to install Playwright browsers.")
        sys.exit(1)

    # Test import
    try:
        from web_scraping_template import WebScraper

        print("✓ Template import test successful")
    except ImportError as e:
        print(f"✗ Template import test failed: {e}")
        sys.exit(1)

    print("\nInstallation completed successfully!")
    print("\nNext steps:")
    print("1. Review the examples in the examples/ directory")
    print("2. Create your own scraping script:")
    print("   from web_scraping_template import WebScraper")
    print("3. Check README.md for detailed usage instructions")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
