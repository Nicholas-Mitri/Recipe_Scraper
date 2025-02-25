"""
PDF Recipe Extractor for Chef's Plate

This script extracts and downloads PDF versions of recipes from Chef's Plate website.
It reads a list of recipe URLs from a text file, visits each URL using Selenium WebDriver,
extracts the PDF download link from the page, and downloads the PDF to a local directory.

The script handles:
- Reading recipe URLs from a file (typically generated by the recipe crawler)
- Navigating to each recipe page with a headless Chrome browser
- Extracting the PDF download link from the page
- Downloading and saving the PDF with an appropriate filename
- Managing errors and providing progress feedback

Usage:
    python extract_pdf_url.py

Requirements:
    - Selenium WebDriver
    - Chrome browser
    - webdriver_manager
    - requests
    - selectorlib
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import requests
from selectorlib import Extractor


def read_recipe_urls(filename):
    """Read recipe URLs from a text file."""
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]


def download_recipe_pdf(url, output_dir):
    """Extract and download recipe PDF from a recipe URL."""
    # Extract recipe name from URL for the PDF filename
    recipe_name = url.split("/")[-1]
    pdf_filename = os.path.join(output_dir, f"{recipe_name}.pdf")

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    print(f"Extracting PDF download link from {url}...")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    try:
        # Load the page
        driver.get(url)

        # Wait for the page to fully load
        # Adjust the wait time as needed
        time.sleep(5)

        # Additional wait for any dynamic content
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Load the extraction rules from the YAML file
        extractor = Extractor.from_yaml_file("extract.yaml")

        # Extract the recipe card download link
        extracted_data = extractor.extract(driver.page_source)

        # Check if we found a recipe card download link
        if extracted_data and extracted_data.get("recipe_link"):
            download_link = extracted_data["recipe_link"]
            print(f"Found recipe card download link: {download_link}")

            # Download the PDF using the recipe card download link
            if extracted_data and extracted_data.get("recipe_link"):
                download_link = extracted_data["recipe_link"]
                print(f"Found recipe card download link: {download_link}")

                try:
                    # Extract recipe name from URL for the filename
                    recipe_name = url.split("/")[-1]
                    if not recipe_name:
                        recipe_name = url.split("/")[-2]

                    # Create a clean filename
                    pdf_filename = f"{recipe_name}.pdf"
                    pdf_path = os.path.join(output_dir, pdf_filename)

                    # Download the PDF
                    response = requests.get(download_link)
                    if response.status_code == 200:
                        with open(pdf_path, "wb") as pdf_file:
                            pdf_file.write(response.content)
                        print(f"Successfully downloaded PDF to {pdf_path}")
                    else:
                        print(
                            f"Failed to download PDF: HTTP status {response.status_code}"
                        )
                except Exception as e:
                    print(f"Error downloading PDF: {e}")
        else:
            print("No recipe card download link found on this page")

    except Exception as e:
        print(f"Error extracting PDF from {url}: {e}")
    finally:
        driver.quit()


def main():
    # Get the latest recipe file
    import glob
    from datetime import datetime

    recipe_files = glob.glob("recipes_*.txt")
    if not recipe_files:
        print("No recipe files found.")
        return

    # Use the most recent file
    latest_file = max(recipe_files)
    print(f"Using recipe file: {latest_file}")

    # Create output directory
    output_dir = "recipe_pdfs"
    os.makedirs(output_dir, exist_ok=True)

    # Read URLs and download PDF for each recipe
    urls = read_recipe_urls(latest_file)
    print(f"Found {len(urls)} recipes to download")

    for url in urls:
        download_recipe_pdf(url, output_dir)
        # Add a delay between requests to be respectful to the server
        time.sleep(2)

    print(f"All recipe PDFs downloaded and saved in {output_dir}")


if __name__ == "__main__":
    main()
