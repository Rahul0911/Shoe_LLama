import asyncio

from playwright.async_api import async_playwright, Playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto('https://blog.roboflow.com/detect-small-objects/')

        await browser.close()

asyncio.run(run())