from playwright.sync_api import sync_playwright
import csv

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    with open("news.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link"])

        # Loop through pages
        for _ in range(3):  # scrape 3 pages
            page.goto("https://news.ycombinator.com")
            page.wait_for_selector(".titleline")

            titles = page.locator(".titleline a").all_text_contents()
            links = page.locator(".titleline a").evaluate_all(
                "elements => elements.map(e => e.href)"
            )

            for title, link in zip(titles, links):
                writer.writerow([title, link])

            # Click "More" button
            page.click("a.morelink")

    browser.close()