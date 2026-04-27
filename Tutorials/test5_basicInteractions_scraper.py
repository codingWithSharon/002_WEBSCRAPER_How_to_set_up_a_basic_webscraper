  
from playwright.sync_api import sync_playwright
import csv

def accept_google_cookies(page):
    try:
        page.locator("button#L2AGLb").click(timeout=3000)
    except:
        pass

def set_english_if_needed(page):
    for txt in ["English", "Engels", "In English"]:
        try:
            page.locator(f"text={txt}").first.click(timeout=2000)
            break
        except:
            pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    context = browser.new_context(
        locale="en-US",
        extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
    )

    page = context.new_page()
    page.goto("https://www.google.com/ncr")

    set_english_if_needed(page)
    accept_google_cookies(page)

    page.fill("textarea[name='q']", "playwright python")
    page.keyboard.press("Enter")

    page.wait_for_selector("h3")

    results = page.locator("h3").all_text_contents()

    # Save to CSV
    with open("google_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "title"])

        for i, title in enumerate(results[:5], 1):
            writer.writerow([i, title])

    print("Saved to google_results.csv")

    browser.close()