# Chef's Plate Recipe Scraper

This project is designed to crawl the Chef's Plate website, collect recipe URLs, and download recipe cards in PDF format. It consists of two main components:

1. A web crawler that systematically explores the Chef's Plate website to collect recipe URLs
2. A PDF extractor that visits each recipe page and downloads the recipe card as a PDF

## Features

- Respectful web crawling with appropriate delays and user agent identification
- Systematic exploration of the Chef's Plate website to discover recipe pages
- Extraction of PDF recipe cards using Selenium WebDriver
- Organized storage of downloaded recipe PDFs

## Requirements

- Python 3.6+
- Required Python packages (install via `pip install -r requirements.txt`):
  - requests
  - beautifulsoup4
  - selenium
  - webdriver_manager
  - selectorlib

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/Recipe_Scraper.git
   cd Recipe_Scraper
   ```

2. Create and activate a virtual environment (recommended):

   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```
   pip install requests beautifulsoup4 selenium webdriver_manager selectorlib
   ```

4. Make sure you have Chrome browser installed (required for Selenium WebDriver)

## Usage

### Step 1: Crawl the Chef's Plate website to collect recipe URLs

Run the crawler script to discover recipe URLs:

```
python recipe_crawl.py
```

This will:

- Start crawling from the Chef's Plate homepage
- Discover recipe URLs throughout the website
- Save the discovered URLs to a text file (e.g., `recipes_2023-04-15.txt`)

### Step 2: Download recipe PDFs

After collecting the recipe URLs, run the PDF extractor script:

```
python extract_pdf_url.py
```

This will:

- Read the most recent recipe URL file
- Visit each recipe page using a headless Chrome browser
- Extract the PDF download link
- Download and save the recipe card as a PDF in the `recipe_pdfs` directory

## Project Structure

- `recipe_crawl.py`: Web crawler for collecting recipe URLs
- `extract_pdf_url.py`: Script for extracting and downloading recipe PDFs
- `extract.yaml`: YAML configuration file for the PDF extractor
- `recipe_pdfs/`: Directory where downloaded recipe PDFs are stored
- `recipes_*.txt`: Text files containing discovered recipe URLs

## Notes

- The crawler is designed to be respectful to the Chef's Plate website by implementing delays between requests
- The PDF extractor uses Selenium WebDriver with a headless Chrome browser to navigate to recipe pages
- This project is for personal use only and should be used in accordance with Chef's Plate's terms of service
