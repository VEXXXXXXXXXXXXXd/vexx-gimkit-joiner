from playwright.sync_api import sync_playwright
import time

def join_gimkit(code, name):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Open Gimkit join page
            page.goto("https://www.gimkit.com/join")

            # Fill room code
            page.fill("input[name='code']", code)
            page.click("button[type='submit']")

            time.sleep(1)

            # Fill name
            page.fill("input[name='name']", name)
            page.click("button[type='submit']")

            time.sleep(2)

            browser.close()
            return True, "Joined successfully"
    except Exception as e:
        return False, str(e)
