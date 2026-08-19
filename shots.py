import asyncio
from playwright.async_api import async_playwright
import pathlib

OUT = pathlib.Path(r"C:\Users\nikk\Projects\portfolio\assets")
OUT.mkdir(parents=True, exist_ok=True)

targets = [
    ("esm", "https://inknikk.github.io/esm-thesis-compare/", 1440, 900),
    ("strata", "https://strata-xi.vercel.app/", 1440, 900),
]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, url, w, h in targets:
            pg = await b.new_page(viewport={"width": w, "height": h})
            try:
                await pg.goto(url, wait_until="networkidle", timeout=30000)
            except Exception:
                await pg.goto(url, timeout=30000)
            await pg.wait_for_timeout(1500)
            path = OUT / f"{name}.png"
            await pg.screenshot(path=str(path), full_page=False)
            print("saved", name, path.stat().st_size)
            await pg.close()
        await b.close()

asyncio.run(main())
