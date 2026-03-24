from playwright.sync_api import sync_playwright
from tools import login_to_lre, open_report, extract_table_to_excel

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # visible browser
        context = browser.new_context()
        page = context.new_page()
         # Increase timeouts to 120 seconds for slow pages
        page.set_default_navigation_timeout(20000)
        page.set_default_timeout(20000)

        login_to_lre(page)

        # Step 2: Open report (new tab)
        report_page = open_report(page)

        # Step 3: Extract table → Excel
        extract_table_to_excel(report_page)

        # Keep both tabs open for inspection
        input("Press ENTER to close...")



        browser.close()


if __name__ == "__main__":
    run()
