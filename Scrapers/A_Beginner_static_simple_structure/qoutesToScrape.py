import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
import time
import os

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://quotes.toscrape.com/")

    all_quotes = []

    while True:
        quotes = page.query_selector_all("div.quote")

        for quote in quotes:
            text = quote.query_selector("span.text").inner_text()
            author = quote.query_selector("small.author").inner_text()
            print(text, "-", author)

            all_quotes.append([text, author])

        next_button = page.query_selector("li.next a")

        if next_button is None:
            print("No more pages. Scraping done!")
            break

        next_button.click()
        page.wait_for_timeout(2000)  # wait for next page

                # === Save to existing DataStorage folder ===
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quotes_all_pages_{timestamp}.csv"
        
        # Use the existing DataStorage folder
        filepath = os.path.join("DataStorage", filename)
        
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Text", "Author"])
            writer.writeheader()
            writer.writerows(all_quotes)
        
        print(f"\n Scraping finished successfully!")
        print(f"Total quotes scraped: {len(all_quotes)}")
        print(f"File saved: {filepath}")

    browser.close()