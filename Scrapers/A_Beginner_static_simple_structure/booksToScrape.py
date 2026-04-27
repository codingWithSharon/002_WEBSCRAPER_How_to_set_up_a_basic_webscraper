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

# =========================================================[PAGINATION HANDLING]=========================================================

import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
import time
import os

def scrape_all_books():
    url = "https://books.toscrape.com/"
    
    # ensure DataStorage exists (same as your other scraper)
    os.makedirs("DataStorage", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto(url, wait_until="networkidle")
        time.sleep(2)
        
        all_books = []
        page_number = 1
        
        while True:
            print(f"Scraping page {page_number}...")
            
            books_on_page = page.locator("article.product_pod").all()
            
            for book in books_on_page:
                try:
                    title = book.locator("h3 a").get_attribute("title")
                    price = book.locator(".price_color").inner_text()
                    
                    rating_class = book.locator(".star-rating").get_attribute("class")
                    rating = rating_class.replace("star-rating", "").strip() if rating_class else "N/A"
                    
                    availability = book.locator(".instock.availability").inner_text().strip()
                    
                    link = book.locator("h3 a").get_attribute("href")
                    full_link = "https://books.toscrape.com/" + link.lstrip("/")
                    
                    all_books.append({
                        "Title": title,
                        "Price": price,
                        "Rating": rating,
                        "Availability": availability,
                        "Product_Link": full_link
                    })
                except Exception as e:
                    print(f"Error on page {page_number}: {e}")
            
            next_button = page.locator("li.next a")
            
            if next_button.count() == 0:
                print("No more 'Next' button found. Scraping completed!")
                break
            
            next_button.click()
            page.wait_for_load_state("networkidle")
            time.sleep(1.5)
            
            page_number += 1
        
        browser.close()
        
        # ✅ FIXED timestamp format (matches your quotes scraper)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"books_all_pages_{timestamp}.csv"
        filepath = os.path.join("DataStorage", filename)
        
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["Title", "Price", "Rating", "Availability", "Product_Link"]
            )
            writer.writeheader()
            writer.writerows(all_books)
        
        print(f"\nScraping finished successfully!")
        print(f"Total books scraped: {len(all_books)}")
        print(f"File saved: {filepath}")

if __name__ == "__main__":
    scrape_all_books()