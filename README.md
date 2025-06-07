# SEO Internal Link Crawler

A powerful SEO crawler designed to analyze the internal link structure of websites. This tool crawls multiple websites asynchronously, extracts internal links, and identifies incorrect or inconsistent internal linking patterns. It also checks the HTTP status codes of target URLs to detect broken or problematic links.

## Features

- Asynchronous crawling of multiple URLs for fast performance
- Extraction of internal links with anchor text
- Identification of inconsistent internal link targets
- HTTP status check for all target URLs
- Saves results in JSON format for easy analysis

## Requirements

- Python 3.8+

You can install dependencies using:

```bash
pip install -r requirements.txt


## Usage and Workflow
This project consists of several main scripts. Here is the recommended order and description of how to use each:

1. InternalLinkScraper.py
Purpose:
Crawls the given websites asynchronously and extracts internal links with their anchor texts.

Usage:
Run the script to generate a JSON file (usually named a.json) containing the raw data of internal links grouped by keywords or pages.

Output:
a.json — A dictionary of extracted internal links and associated URLs.

2. LinkAnalyzer.py
Purpose:
Analyzes the extracted data in a.json to detect inconsistent or incorrect internal linking patterns. It categorizes keywords into groups based on link counts and frequency of target URLs.

Usage:
Run after generating a.json.

Output:

b.txt — Lists keywords with inconsistent target URLs where most have a majority correct target but some have wrong ones.

c.txt — Lists keywords with fewer than 4 items and their associated URLs.

3. DeadLinkDetector.py
Purpose:
Checks HTTP status codes for target URLs found in a.json to identify dead or problematic links.

Usage:
Run after generating a.json (and optionally after or alongside LinkAnalyzer.py).

Output:
d.json — Contains target URLs with non-200 HTTP status codes and the URLs that refer to them.

4. LinkExtractor.py
Purpose:
Extracts all links from web page content as a helper utility that can feed data into other scripts or be used independently.

Usage:
Run to produce a JSON output of links from given pages or inputs.

Output:
JSON file containing extracted links from pages.

Note:
Make sure the input files (like a.json) exist before running dependent scripts. Also, install all required dependencies.


