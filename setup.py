#!/usr/bin/env python3
"""
Setup script for Web Scraping Template
"""

from setuptools import setup, find_packages

setup(
    name="web_scraping_template",
    version="1.0.0",
    description="A reusable, configurable web scraping template with Playwright.",
    author="thoni-dev",
    url="https://github.com/thoni-miguel/web-scraping-template",
    packages=find_packages(),
    install_requires=[
        "playwright>=1.42.0",
        "beautifulsoup4>=4.12.3",
        "pandas>=2.2.0",
        "pyyaml>=6.0.1",
        "requests>=2.32.0",
        "openpyxl>=3.1.2",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
