"""
Amazon Fashion Spy — Main orchestrator
Designed to run as a Claude Code Remote Routine at 6:00 AM Panama time.
Uses requests+BeautifulSoup (no browser needed).
"""

import json
from datetime import datetime
from pathlib import Path

from categories import CATEGORIES
from scraper_http import run_scraper
from scorer import score_panama, estimate_monthly_sales
from report import generate_html


REPORTS_DIR = Path(__file__).parent / "reports"
DOCS_DIR    = Path(__file__).parent.parent / "docs"


def enrich(products: list[dict], category: dict) -> list[dict]:
    enriched = []
    for p in products:
        p["monthly_sales_est"] = estimate_monthly_sales(p.get("rank", 50))
        p["panama"] = score_panama(p, category)
        enriched.append(p)
    return enriched


def print_summary(all_products: dict) -> None:
    total = sum(len(v) for v in all_products.values())
    print(f"\n{'='*55}")
    print(f"  AMAZON SPY — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Total productos: {total}")
    print(f"{'='*55}")
    for cat in CATEGORIES:
        prods = all_products.get(cat["id"], [])
        if prods:
            top = prods[0]
            print(
                f"  {cat['emoji']} {cat['name']:22s} "
                f"{len(prods):>3} prods | "
                f"top 🇵🇦 {top['panama']['score']}/100"
            )
    print(f"{'='*55}\n")


def main() -> None:
    now = datetime.utcnow()
    print(f"\n🚀 Amazon Spy — {now.strftime('%Y-%m-%d %H:%M UTC')}")

    # 1 — Scrape (requests-based, no browser needed)
    raw = run_scraper(CATEGORIES)

    # 2 — Enrich with Panama score
    cat_map = {c["id"]: c for c in CATEGORIES}
    all_products = {
        cat_id: enrich(prods, cat_map[cat_id])
        for cat_id, prods in raw.items()
    }

    total = sum(len(v) for v in all_products.values())
    if total == 0:
        print("⚠️  No products found — Amazon may be blocking. Report skipped.")
        return

    print_summary(all_products)

    # 3 — Generate HTML report
    REPORTS_DIR.mkdir(exist_ok=True)
    date_slug = now.strftime("%Y-%m-%d")
    html = generate_html(all_products, CATEGORIES, now)

    (REPORTS_DIR / f"{date_slug}.html").write_text(html, encoding="utf-8")
    (REPORTS_DIR / "latest.html").write_text(html, encoding="utf-8")

    # 4 — Save JSON
    (REPORTS_DIR / f"{date_slug}.json").write_text(
        json.dumps(all_products, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 5 — Publish to GitHub Pages
    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / ".nojekyll").touch()
    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")

    print(f"✅ Reporte generado: {date_slug}")
    print(f"✅ GitHub Pages actualizado: docs/index.html")
    print("\n🏁 Done.\n")


if __name__ == "__main__":
    main()
