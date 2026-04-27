# PLEASE READ ME

## Introduction

If you have followed the previous project 001_AT_How_to_set_up_a_test_automation_project than you know how to find locators and use them. For webscraping locators are just as important so if you haven't yet looked at the previous project in this series I strongly recommend that you do.

### Difference bewteen automation testing and scraping

Test automation verifies expected behavior on controlled environments; web scraping extracts unknown data from unpredictable live sites. Testing uses assertions and fixed flows; scraping handles missing data, infinite pagination, and adds delays to be polite. Testing asks "does it work?" — scraping asks "what can I get?"

## What you will learn

In this roject you will learn what a webscraper is and how to set one up. In this project we will use Playwright with Python.

## What is a webscraper?

In one line a webscraper basically automatically pulls data from a webpage.

What the webscraper does:

    - Opens a page
    - Reads the HTML content
    - Extracts specific data

## Setup + Tutorial

### Step 1 Create a folder and name it as you please
### Step 2 Open the folder in with VS Code
### Step 3 Install the following using te termnial commands as shown below:

    - python --version
    - python -m venv venv
    - pip install playwright (installs packages)
    - Playwright install (insalls browsers)

### Step 4 Create a file calles "test1_basic_pagTitle_scraper.py"
### Step 5 Paste the following in that file:

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://example.com")
        print(page.title())
        browser.close()

### Step 6 Run the script by using the command "python test1_basic_pagTitle_scraper.py" 

    We expect the page title to be printed in the terminal. If this happens you know that you got a working setup.

### Step 7 Create a second file called "test2_basic_titles_scraper_savingToText.py.py"

    Paste the following script in the file:

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

### Step 8 Upgrade script by saving the scraped content to a file

    with open("titles.txt", "w", encoding="utf-8") as f:
        for title in titles:
            f.write(title + "\n")

    After running the file "test2_basic_titles_scraper_savingToText.py" for the second time with this addition you should see that a new text file has been created in the Explorer. If you open it you should see the titles listed in that file. This means you have successfully saved the scraped content to a textfile.

### Step 9 Structure the data

    Now that we can scrape and save data to a file the next step is learning how to structure it. It would be better to save the scraped content to a CSV format. So create a new file called "test3_basic_titles_scraper_savingToCSV.py" We can achieve that by using the following script:

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

### Step 10 Looping through pages

    Create another file called "test4_loopthroughMultiplePages_scraper.py" and paste the following script into it:

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
     
### TIP! When you are running these scripts you want to look human, you can do that by adding delays:
    "page.wait_for_timeout(1000)  # 1 second" 

### Step 11 Interactions

    To create a more powerfull script you want to interact with the page elements, just like in an automated E2E test. Create a file and name it "test5_basicInteractiond_scraper.py" and paste the following in the file:

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com")

        # Accept cookies if it appears (important)
        try:
            page.click("text=Accept all", timeout=3000)
        except:
            pass

        # Type into search box
        page.fill("textarea[name='q']", "playwright python")

        # Press Enter
        page.keyboard.press("Enter")

        # Wait for results
        page.wait_for_selector("h3")

        # Get results
        results = page.locator("h3").all_text_contents()

        for i, r in enumerate(results[:5], start=1):
            print(f"{i}. {r}")

    browser.close()

## Step 12 Initialize repository
    Enter command "git init" 
## Step 13 Stage ALL changes
    Enter command "git add ." or if you just want to stage a specific file use command like this "git add filename.py"
## Step 14 Commit changes
    Enter command "git commit -m "Initial commit message""
## Step 15 Push changes
    Enter command "git push origin main"
## Step 16 Publish (decide private or public) to your github
    Enter command git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
## Step 17 Create a branch
    You should create a branch where you can work from. If you want to move back to the main branch use the following command "git checkout main" and when you want to check out your feature branch again use the same command but then selecting your branchname "git checkout feature/building_A_Real_Webscraper"

## Architecture

When a project grows, we need good architecture to keep the project readable and maintainable. So before we move on with building the project further we need to now decide the route we

## Pitfalls

### Common beginner issues during execution

    - Selector returns empty list > wrong CSS selector
    - Page loads slowly > need wait_for_selector
    - Dynamic sites > need scrolling/clicking

## Links

### Great websites to practice scraping

    - https://books.toscrape.com/
    - https://quotes.toscrape.com/
    - https://www.scrapethissite.com/pages/
    - https://quotes.toscrape.com/login
    - https://webscraper.io/test-sites/e-commerce/allinone
    - https://httpbin.org/
    - https://news.ycombinator.com/
    - https://nl.indeed.com/ 


