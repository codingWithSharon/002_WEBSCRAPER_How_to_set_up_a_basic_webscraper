from playwright.sync_api import sync_playwright

def test_baseTemplate_open():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.ad.nl/", wait_until="domcontentloaded") # <-- Change URL for desired website

        # cookie banner (safe)
        try:
            page.locator("button:has-text('Akkoord')").click(timeout=5000) # <--Change selector and text for cookie banner on target website
            print("Cookie banner accepted")
        except:
            print("No cookie banner")

        page.wait_for_timeout(5000)

        print("Page loaded:", page.title())

        browser.close()

if __name__ == "__main__":
    test_baseTemplate_open()