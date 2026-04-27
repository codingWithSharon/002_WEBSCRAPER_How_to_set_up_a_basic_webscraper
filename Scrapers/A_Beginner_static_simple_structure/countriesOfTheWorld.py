from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.scrapethissite.com/pages/simple/")

    page.wait_for_timeout(2000)

    countries = page.query_selector_all("div.country")

    all_countries = []

    for country in countries:
        name = country.query_selector("h3.country-name").inner_text().strip()
        all_countries.append(name)

    print(all_countries)

    browser.close()