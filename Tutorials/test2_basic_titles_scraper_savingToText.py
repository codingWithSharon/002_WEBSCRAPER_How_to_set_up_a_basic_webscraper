from playwright.sync_api import sync_playwright
import os
from datetime import datetime

# Make sure the folder exists
os.makedirs("DataStorage", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://news.ycombinator.com")

    # Grab all headlines
    titles = page.locator(".titleline a").all_text_contents()

    # Print them
    for i, title in enumerate(titles, start=1):
        print(f"{i}. {title}")

    # Dynamic filename
    filename = f"titles_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    file_path = os.path.join("DataStorage", filename)

    # Save the titles to a file
    with open(file_path, "w", encoding="utf-8") as f:
        for title in titles:
            f.write(title + "\n")

    browser.close()