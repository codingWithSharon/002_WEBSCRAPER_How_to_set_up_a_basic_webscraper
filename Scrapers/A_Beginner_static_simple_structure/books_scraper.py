# Command for runnning the scraper: python Scrapers\A_Beginner_static_simple_structure\books_scraper.py

# =========================================================[LAUNCHING THE PAGE]=========================================================
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://books.toscrape.com/")

    page.wait_for_timeout(5000)  # just to see it
    browser.close()

# =========================================================[SCRAPING THE DATA]=========================================================

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://books.toscrape.com/")

    books = page.query_selector_all("article.product_pod")

    for book in books:
        title = book.query_selector("h3 a").get_attribute("title")
        price = book.query_selector(".price_color").inner_text()

        print(title, price)

    browser.close()

# =========================================================[SAVING THE DATA]=========================================================
from playwright.sync_api import sync_playwright
from datetime import datetime
import os
import csv

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://books.toscrape.com/")

    books = page.query_selector_all("article.product_pod")
    
    # Create lists to store data
    titles = []
    links = []

    for book in books:
        title = book.query_selector("h3 a").get_attribute("title")
        price = book.query_selector(".price_color").inner_text()
        
        # Get the link href attribute
        link = book.query_selector("h3 a").get_attribute("href")
        
        print(title, price)
        
        titles.append(title)
        links.append(link)

    # Create DataStorage folder if it doesn't exist
    os.makedirs("DataStorage", exist_ok=True)
    
    # Dynamic filename with timestamp
    filename = f"books_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    file_path = os.path.join("DataStorage", filename)

    # Save to CSV inside DataStorage folder
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link"])

        # Fixed indentation and variable names
        for title, link in zip(titles, links):
            writer.writerow([title, link])
        
    browser.close()