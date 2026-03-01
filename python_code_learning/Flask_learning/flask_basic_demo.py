import asyncio
from flask import Flask, jsonify, request
from playwright.async_api import async_playwright

app = Flask(__name__)


# -----------------------------
# Async function to search Bing
# -----------------------------
async def search_bing(query):
    results_data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Open Bing
        await page.goto("https://www.bing.com", wait_until="domcontentloaded")

        # Locate search box
        search_box = page.locator('xpath=//*[@id="sb_form_q"]')
        await search_box.wait_for()

        # Fill search query
        await search_box.fill(query)
        await page.keyboard.press("Enter")

        # Wait for search results
        results = page.locator("//li[@class='b_algo']")
        await results.first.wait_for()

        count = await results.count()

        for i in range(min(5, count)):
            title = await results.nth(i).locator("xpath=.//h2").inner_text()
            link = await results.nth(i).locator("xpath=.//h2/a").get_attribute("href")

            results_data.append({
                "rank": i + 1,
                "title": title,
                "link": link
            })

        await browser.close()

    return results_data


# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return "Flask Bing Search API Running!"


# -----------------------------
# Search Route
# -----------------------------
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")

    if not query:
        return jsonify({
            "status": "error",
            "message": "Please provide search query using ?q="
        }), 400

    try:
        results = asyncio.run(search_bing(query))
        return jsonify({
            "status": "success",
            "query": query,
            "results": results
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)