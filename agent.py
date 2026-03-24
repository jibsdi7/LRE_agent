from playwright.sync_api import sync_playwright
from tools import login_to_lre, open_report, extract_table_to_excel
from ollama_agent import decide_steps


def run_agent(prompt):
    # 🧠 Get steps from Ollama
    try:
        steps = decide_steps(prompt)
    except Exception as e:
        print("❌ Failed to get steps from Ollama:", e)
        return

    print("🧠 Steps from AI:", steps)

    # Validate steps
    if not isinstance(steps, list):
        print("❌ Invalid steps format")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        report_page = None

        # 🔁 Execute steps
        for step in steps:
            try:
                tool = step.get("tool")

                if tool == "login":
                    print("🔐 Logging in...")
                    login_to_lre(page)

                elif tool == "open_report":
                    print("📊 Opening report...")
                    report_page = open_report(page)

                elif tool == "extract_table":
                    print("📥 Extracting table...")
                    if report_page:
                        extract_table_to_excel(report_page)
                    else:
                        print("⚠️ Report page not available")

                else:
                    print(f"⚠️ Unknown tool: {tool}")

            except Exception as e:
                print(f"❌ Error in step {step}: {e}")

        input("Press ENTER to close...")
        browser.close()


if __name__ == "__main__":
    prompt = input("Enter command: ")
    run_agent(prompt)