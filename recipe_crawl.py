"""
Recipe Crawler for Chef's Plate

This script crawls the Chef's Plate website to collect recipe URLs.
It starts from the base URL and systematically explores the site,
extracting links to recipe pages. The discovered recipe URLs are
saved to a text file with a timestamp for later processing.

The crawler respects the website by implementing delays between requests
and uses a proper user agent to identify itself.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

URL = "https://www.chefsplate.com/"


def crawl_domain(base_url, max_pages=100):
    """
    Crawl a domain and collect all links within that domain.

    Args:
        base_url: The starting URL to crawl
        max_pages: Maximum number of pages to crawl (to prevent infinite crawling)

    Returns:
        A set of all discovered URLs within the domain
    """
    # Parse the base domain
    base_domain = urlparse(base_url).netloc
    recipes = []
    # Track visited and to-visit URLs
    visited_urls = set()
    urls_to_visit = {base_url}
    found_urls = set()

    # Limit the number of pages to crawl
    page_count = 0

    # Add a user agent to avoid being blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    while urls_to_visit and page_count < max_pages:
        # Get the next URL to visit
        current_url = urls_to_visit.pop()

        # Skip if already visited
        if current_url in visited_urls:
            continue

        print(f"Crawling: {current_url}")

        try:
            # Add a small delay to be respectful to the server
            time.sleep(1)

            # Fetch the page
            response = requests.get(current_url, headers=headers)

            # Skip if not successful
            if response.status_code != 200:
                print(
                    f"Failed to fetch {current_url}: Status code {response.status_code}"
                )
                visited_urls.add(current_url)
                continue

            # Parse the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Mark as visited
            visited_urls.add(current_url)
            found_urls.add(current_url)
            page_count += 1

            # Find all links
            for link in soup.find_all("a", href=True):
                href = link.get("href")
                if not href:
                    continue

                # Convert relative URLs to absolute URLs
                absolute_link = urljoin(current_url, href)

                # Parse the link
                parsed_link = urlparse(absolute_link)

                # Skip fragments, query parameters, etc. to avoid duplicates
                clean_link = (
                    f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}"
                )

                # Only follow links within the same domain and with specific paths
                if parsed_link.netloc == base_domain:

                    if clean_link not in visited_urls:
                        urls_to_visit.add(clean_link)
                        found_urls.add(clean_link)
                    # Extract recipe data if it's a recipe page
                    if "/recipes/" in parsed_link.path:
                        try:
                            print(f"Found recipe: {clean_link}")
                            recipes.append(clean_link)
                        except Exception as e:
                            print(
                                f"Error extracting recipe data from {clean_link}: {e}"
                            )

        except Exception as e:
            print(f"Error crawling {current_url}: {e}")

    return recipes


if __name__ == "__main__":
    recipes = crawl_domain(URL, max_pages=50)

    print("\nAll discovered recipe links:")
    for link in sorted(recipes):
        print(link)

        # Save recipes to a file with today's date
        from datetime import datetime

        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"recipes_{today}.txt"

        with open(filename, "w") as f:
            for link in sorted(recipes):
                f.write(f"{link}\n")

        print(f"\nRecipes saved to {filename}")
