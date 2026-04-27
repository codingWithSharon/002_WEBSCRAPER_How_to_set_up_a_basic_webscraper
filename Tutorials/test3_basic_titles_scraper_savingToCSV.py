from playwright.sync_api import sync_playwright
import csv
import os
from datetime import datetime

# Make sure the folder exists
os.makedirs("DataStorage", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://news.ycombinator.com")

    # Wait for content (important for real sites)
    page.wait_for_selector(".titleline")

    titles = page.locator(".titleline a").all_text_contents()
    links = page.locator(".titleline a").evaluate_all(
        "elements => elements.map(e => e.href)"
    )

    # Dynamic filename with timestamp
    filename = f"news_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    file_path = os.path.join("DataStorage", filename)

    # Save to CSV inside DataStorage folder
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link"])

        for title, link in zip(titles, links):
            writer.writerow([title, link])

    browser.close()