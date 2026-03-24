from playwright.sync_api import Page
import pandas as pd
import os

def login_to_lre(page: Page):
    page.goto("https://lre.us.royalahold.net/Loadtest/pcx/login")

    page.fill("#username-input", "vn43075")
    page.fill("#password-input", "Welcome123")
    page.click("button[type='submit']")
    #page.click("#Authenticate")

    page.locator("#domain-input").click()
    page.locator("text=Infrastructure").click()

    # Wait and select Power BI
    page.locator("#project-input").click()
    page.wait_for_timeout(5000)
    page.locator("text=PowerBI").click()
    
    page.click("button[type='submit']")
    
    page.get_by_role("heading", name="Home Page").wait_for()
    
    print("✅ Logged in")


def open_report(page):
   # with page.expect_popup() as popup_info:
   #  page.get_by_role(
   #      "button",
   #      name="Click to open the Run Dashboard page"
   #  ).first.click()

   #  report_page = popup_info.value
   #  report_page.wait_for_load_state()
   with page.expect_popup() as popup_info:
    page.locator("button.hover-action-btn").first.click()

    report_page = popup_info.value
    report_page.wait_for_load_state()
    print("✅ Report opened in new tab")
    print("URL:", report_page.url)

    return report_page


def extract_table_to_excel(report_page):


    # Wait for frames to load
    report_page.wait_for_timeout(3000)

    # 🔍 Find correct frame
    target_frame = None

    for frame in report_page.frames:
        print("Frame URL:", frame.url)

        if "summary.html" in frame.url:
            target_frame = frame
            break

    if not target_frame:
        raise Exception("❌ summary.html frame not found")

    print("✅ Found summary frame")

    # Wait for table inside frame
    target_frame.wait_for_selector("#TransactionsTable")

    # Extract headers
    headers = target_frame.locator("#TransactionsTable thead th").all_text_contents()

    # Extract rows
    rows = target_frame.locator("#TransactionsTable tbody tr")

    data = []

    for i in range(rows.count()):
        row = rows.nth(i)
        cells = [c.strip() for c in row.locator("td").all_text_contents()]
        data.append(cells)

    # Save to Excel
    df = pd.DataFrame(data, columns=headers)
    df.to_excel("output/report.xlsx", index=False)

    print("✅ Excel created successfully")