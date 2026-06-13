"""
HTTP-based Amazon scraper using requests + BeautifulSoup.
No browser needed — works in any Python environment.
Amazon's Best Sellers pages are server-side rendered, so the initial
HTML already contains the full product list.
"""

import re
import time
import random
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def _parse_products(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    products = []
    seen_asins = set()

    # Amazon Best Sellers — multiple possible container selectors
    item_selectors = [
        "li.zg-item-immersion",
        "div.zg-grid-general-faceout",
        "div[class*='zg-item']",
        "div[class*='p13n-grid']",
        "div[class*='zg-grid']",
        "div[class*='_cDEzb_grid-cell']",
    ]

    items = []
    for sel in item_selectors:
        items = soup.select(sel)
        if len(items) >= 3:
            break

    # Last-resort: any element with a data-asin that contains a product link
    if len(items) < 3:
        items = [el for el in soup.select("[data-asin]")
                 if el.get("data-asin") and el.select_one("a[href*='/dp/']")]

    for idx, item in enumerate(items[:35]):
        # ASIN — from data-asin or product URL
        asin = item.get("data-asin", "")
        if not asin:
            link_el = item.select_one("a[href*='/dp/']")
            if link_el:
                m = re.search(r"/dp/([A-Z0-9]{10})", link_el["href"])
                asin = m.group(1) if m else ""

        if not asin or asin in seen_asins:
            continue
        seen_asins.add(asin)

        # Title
        title_el = item.select_one(
            "[class*='line-clamp'], .p13n-sc-truncate, "
            "[class*='truncate'], a[title], span[class*='a-size-base']"
        )
        if title_el:
            title = title_el.get("title") or title_el.get_text(strip=True)
        else:
            title = ""
        if not title:
            continue

        # Image
        img_el = item.select_one("img")
        image = img_el.get("src") or img_el.get("data-src", "") if img_el else ""

        # Price
        price_el = item.select_one(
            "[class*='p13n-sc-price'], span.a-price .a-offscreen, "
            "[class*='a-price']"
        )
        price = price_el.get_text(strip=True) if price_el else ""

        # Rating
        rating_el = item.select_one("span.a-icon-alt")
        rating_text = rating_el.get_text() if rating_el else ""
        rm = re.search(r"(\d+\.?\d*)\s*out", rating_text)
        rating = float(rm.group(1)) if rm else 0.0

        # Reviews
        rev_el = item.select_one(
            "span.a-size-small.a-link-normal, "
            "[aria-label*='stars'] + span, span[class*='a-size-small']"
        )
        rev_text = rev_el.get_text(strip=True).replace(",", "") if rev_el else "0"
        rm2 = re.search(r"(\d+)", rev_text)
        reviews = int(rm2.group(1)) if rm2 else 0

        # URL
        link_el = item.select_one("a[href*='/dp/']")
        href = link_el["href"].split("?")[0] if link_el else ""
        url = ("https://www.amazon.com" + href) if href.startswith("/") else href

        products.append({
            "rank": idx + 1,
            "asin": asin,
            "title": title[:120],
            "image": image,
            "price": price,
            "rating": rating,
            "reviews": reviews,
            "url": url,
        })

    return products


def scrape_category(category: dict) -> list[dict]:
    print(f"  → {category['emoji']} {category['name']}...")
    delays = [3, 7, 15]
    for attempt in range(4):
        try:
            resp = SESSION.get(category["url"], timeout=25)

            if resp.status_code == 200 and not any(
                k in resp.text for k in ["Enter the characters", "robot check", "CAPTCHA"]
            ):
                products = _parse_products(resp.text)
                print(f"  ✓  {len(products)} products")
                return products

            if resp.status_code == 503 or resp.status_code == 429:
                if attempt < 3:
                    wait = delays[attempt]
                    print(f"  ⚠️  HTTP {resp.status_code} — retry in {wait}s")
                    time.sleep(wait)
                    continue

            if any(k in resp.text for k in ["Enter the characters", "robot check", "CAPTCHA"]):
                if attempt < 3:
                    wait = delays[attempt]
                    print(f"  ⚠️  Bot check — retry in {wait}s")
                    time.sleep(wait)
                    continue
                print(f"  ✗  Amazon bot check persists — skipping")
                return []

            print(f"  ✗  HTTP {resp.status_code} — skipping")
            return []

        except Exception as e:
            if attempt < 3:
                wait = delays[attempt]
                print(f"  ⚠️  Error ({e}) — retry in {wait}s")
                time.sleep(wait)
            else:
                print(f"  ✗  Error: {e}")
                return []
    return []


def run_scraper(categories: list[dict]) -> dict[str, list[dict]]:
    results = {}
    for cat in categories:
        results[cat["id"]] = scrape_category(cat)
        time.sleep(random.uniform(2.5, 5.0))   # polite delay between categories
    return results
