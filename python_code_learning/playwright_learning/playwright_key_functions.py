from playwright.async_api import async_playwright
import asyncio

print("Playwright key functions demo")

async def playwright_key_function():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=False) #browser will be launched
        page=await browser.new_page() #new page will be opened
        #navigation
        await page.goto("https://www.google.com/")
        await page.wait_for_timeout(3000)
        await browser.close() #browser will be closed

        #css selector
       # Step 1 f12+ or right click +inspect
       # Step 2 element click
         # Step 3 right click copy and select copy selector or copy xpath
         


if __name__ == "__main__":
    asyncio.run(playwright_key_function())
