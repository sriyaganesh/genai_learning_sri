import asyncio
from playwright.async_api import async_playwright
import yagmail
from datetime import datetime


EMAIL = "srividhyaganesan1988@gmail.com"
APP_PASSWORD = "ivhx fpct dyip bhzz"
#TO_EMAIL="vlnarayanan.84@gmail.com"
TO_EMAIL="balavb89@gmail.com"


async def scrape_nse():
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        page = await browser.new_page()

        # Open NSE Nifty 50 page
        await page.goto("https://www.nseindia.com/market-data/live-equity-market")

        await page.wait_for_timeout(5000)

        rows = page.locator("table tbody tr")
        count = await rows.count()

        for i in range(count):
            cols = rows.nth(i).locator("td")
            stock = await cols.nth(0).inner_text()
            close_price = await cols.nth(5).inner_text()

            data.append(f"{stock} - {close_price}")

        await browser.close()

    return data


async def main():
    stock_data = await scrape_nse()
    # ✅ Sort Alphabetically by Stock Name
    stock_data.sort(key=lambda x: x[0].lower())

    # Write to text file
    today = datetime.now().strftime("%Y-%m-%d")
    file_name = f"nse_closing_prices_{today}.txt"

    with open(file_name, "w", encoding="utf-8") as f:
        for line in stock_data:
            f.write(line + "\n")

    print("File created successfully.")

    # Send email
    yag = yagmail.SMTP(EMAIL, APP_PASSWORD)
    yag.send(
        to=TO_EMAIL,
        subject="NSE Closing Prices",
        contents="Attached is today's NSE closing prices.",
        attachments=file_name,
    )

    print("Email sent successfully.")


asyncio.run(main())