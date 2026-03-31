---
name: web-scraper
description: A skill for web scraping and data extraction
license: MIT
version: 1.0.0
author: Demo User
tags:
  - web
  - scraping
  - data-extraction
---

# Web Scraper Skill

## Overview

This skill provides web scraping capabilities for extracting data from web pages.

## Capabilities

- Fetch web pages
- Extract data using CSS selectors
- Handle pagination
- Parse HTML and XML

## Usage

When the agent needs to scrape web pages or extract structured data from websites, this skill will be invoked.

## Implementation

The skill is implemented in the `scripts/` directory with the following functions:

- `scrape_page`: Basic web scraping operation
- `extract_data`: Advanced data extraction with custom selectors

## Examples

### Basic Usage

```
Input: "Scrape data from https://example.com"
Output: Extracted data from the page
```

### Advanced Usage

```
Input: "Extract product prices from https://shop.com"
Output: List of product prices with metadata
```

## Notes

- Respect robots.txt
- Add appropriate delays between requests
- Handle errors gracefully
