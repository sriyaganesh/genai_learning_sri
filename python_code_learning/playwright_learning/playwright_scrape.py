from playwright.sync_api import sync_playwright

URL = "https://www.google.in/"
OUTPUT_FILE = "scrape_paage_content.txt"

def scrape_page(url: str, output_file: str):
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Open URL
        page.goto(url, timeout=60000)

        # Wait for page to load completely
        page.wait_for_load_state("networkidle")

        # Extract visible text content
        content = page.inner_text("body")

        # Write to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        browser.close()
        print(f"Content saved to {output_file}")

if __name__ == "__main__":
    scrape_page(URL, OUTPUT_FILE)