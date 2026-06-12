import asyncio
import random
from playwright.async_api import async_playwright, BrowserContext

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

STEALTH_SCRIPT = """
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
    window.chrome = { runtime: {} };
"""

EXTRACT_SCRIPT = """
() => {
    const results = [];
    const seen = new Set();

    // Multiple selector strategies for Amazon Best Sellers
    const containerSelectors = [
        '.zg-item-immersion',
        '.p13n-gridRow ._cDEzb_grid-cell_1uMOS',
        '[class*="zg-item"]',
        '.s-result-item[data-asin]',
    ];

    let items = null;
    for (const sel of containerSelectors) {
        const found = document.querySelectorAll(sel);
        if (found.length >= 3) { items = found; break; }
    }
    if (!items || items.length === 0) return results;

    items.forEach((item, idx) => {
        const asin = (
            item.getAttribute('data-asin') ||
            item.querySelector('[data-asin]')?.getAttribute('data-asin') ||
            ''
        ).trim();

        if (!asin || seen.has(asin)) return;
        seen.add(asin);

        const titleEl = item.querySelector(
            '._cDEzb_p13n-sc-css-line-clamp-3_g3dy1, ' +
            '.p13n-sc-truncate, ' +
            '.p13n-sc-truncate-desktop-type2, ' +
            'a[title], ' +
            'span.a-size-base-plus'
        );
        const title = (titleEl?.textContent || titleEl?.getAttribute('title') || '').trim();
        if (!title) return;

        const imgEl = item.querySelector('img.p13n-sc-dynamic-image, img[data-a-dynamic-image], img');
        const image = imgEl?.src || imgEl?.getAttribute('data-src') || '';

        const priceEl = item.querySelector(
            '._cDEzb_p13n-sc-price_3mJ9Z, .p13n-sc-price, span.a-price .a-offscreen'
        );
        const price = (priceEl?.textContent || '').trim().replace(/\s+/g, '');

        const ratingEl = item.querySelector('span.a-icon-alt');
        const ratingMatch = (ratingEl?.textContent || '').match(/(\d+\.?\d*)/);
        const rating = ratingMatch ? parseFloat(ratingMatch[1]) : 0;

        const reviewsEl = item.querySelector(
            'span.a-size-small.a-link-normal, span[aria-label*="ratings"], span.a-size-small'
        );
        const reviewsRaw = (reviewsEl?.textContent || '0').replace(/[^0-9]/g, '');
        const reviews = parseInt(reviewsRaw) || 0;

        const linkEl = item.querySelector('a.a-link-normal[href*="/dp/"], a[href*="/dp/"]');
        const href = linkEl?.getAttribute('href') || '';
        const url = href ? 'https://www.amazon.com' + href.split('?')[0] : '';

        const rankEl = item.querySelector('.zg-bdg-text, [class*="zg-badge-number"]');
        const rankText = rankEl?.textContent?.replace(/[^0-9]/g, '') || String(idx + 1);
        const rank = parseInt(rankText) || (idx + 1);

        results.push({ rank, asin, title, image, price, rating, reviews, url });
    });

    return results.slice(0, 40);
}
"""


async def build_context(playwright) -> tuple:
    browser = await playwright.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-first-run",
        ],
    )
    context = await browser.new_context(
        user_agent=USER_AGENT,
        viewport={"width": 1440, "height": 900},
        locale="en-US",
        timezone_id="America/Panama",
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    await context.add_init_script(STEALTH_SCRIPT)
    return browser, context


async def scrape_category(context: BrowserContext, category: dict) -> list[dict]:
    page = await context.new_page()
    products = []

    try:
        print(f"  → Scraping {category['emoji']} {category['name']}...")
        await page.goto(category["url"], wait_until="domcontentloaded", timeout=45000)
        await asyncio.sleep(random.uniform(2.5, 4.5))

        # Detect CAPTCHA or login wall
        page_text = await page.inner_text("body")
        if "Enter the characters" in page_text or "robot" in page_text.lower():
            print(f"  ⚠️  CAPTCHA detected on {category['name']} — skipping")
            return []

        # Scroll to trigger lazy loading
        for _ in range(6):
            await page.mouse.wheel(0, 900)
            await asyncio.sleep(random.uniform(0.6, 1.2))
        await page.mouse.wheel(0, -99999)
        await asyncio.sleep(1.5)

        raw = await page.evaluate(EXTRACT_SCRIPT)
        products = [p for p in raw if p.get("title")]
        print(f"  ✓  {len(products)} products found in {category['name']}")

    except Exception as e:
        print(f"  ✗  Error in {category['name']}: {e}")
    finally:
        await page.close()

    return products


async def run_scraper(categories: list[dict]) -> dict[str, list[dict]]:
    results = {}
    async with async_playwright() as playwright:
        browser, context = await build_context(playwright)
        try:
            for cat in categories:
                products = await scrape_category(context, cat)
                results[cat["id"]] = products
                # Respectful delay between categories
                await asyncio.sleep(random.uniform(3, 6))
        finally:
            await browser.close()
    return results
