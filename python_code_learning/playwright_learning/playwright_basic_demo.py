import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        page = await browser.new_page()

        # Open Bing
        await page.goto("https://www.bing.com")

        # Use your XPath
        search_box = page.locator('xpath=//*[@id="sb_form_q"]')
        await search_box.wait_for()

        # Type search query
        await search_box.fill("SA vs AUS latest update")
        await page.keyboard.press("Enter")

        # Wait for results
        results = page.locator("//li[@class='b_algo']")
        await results.first.wait_for()

        print("\nTop Results:\n")

        count = await results.count()

        for i in range(min(5, count)):
            title = await results.nth(i).locator("xpath=.//h2").inner_text()
            link = await results.nth(i).locator("xpath=.//h2/a").get_attribute("href")
            print(f"{i+1}. {title}")
            print(link)
            print()

        await browser.close()


asyncio.run(main())