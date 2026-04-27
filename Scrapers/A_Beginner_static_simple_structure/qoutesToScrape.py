import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
import os

# create DataStorage folder if it doesn't exist
folder_path = "DataStorage"
os.makedirs(folder_path, exist_ok=True)

# create timestamped filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_path = os.path.join(folder_path, f"quotes_{timestamp}.csv")

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
        page.wait_for_selector("div.quote")

    browser.close()

# save CSV in DataStorage with timestamp
with open(file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Quote", "Author"])
    writer.writerows(all_quotes)

print(f"Data saved to {file_path}")