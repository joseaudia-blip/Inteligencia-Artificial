"""
Amazon Fashion Spy — Main orchestrator
Runs daily via GitHub Actions at 6:00 AM Panama time (11:00 AM UTC).
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from categories import CATEGORIES
from scraper import run_scraper
from scorer import score_panama, estimate_monthly_sales
from report import generate_html


REPORTS_DIR = Path(__file__).parent / "reports"


def enrich(products: list[dict], category: dict) -> list[dict]:
    """Add Panama score and sales estimate to each product."""
    enriched = []
    for p in products:
        p["monthly_sales_est"] = estimate_monthly_sales(p.get("rank", 50))
        p["panama"] = score_panama(p, category)
        enriched.append(p)
    return enriched


def print_summary(all_products: dict[str, list[dict]]) -> None:
    total = sum(len(v) for v in all_products.values())
    print(f"\n{'='*55}")
    print(f"  AMAZON SPY — RESUMEN")
    print(f"{'='*55}")
    print(f"  Total productos encontrados: {total}")
    for cat in CATEGORIES:
        products = all_products.get(cat["id"], [])
        if products:
            top = products[0]
            print(
                f"  {cat['emoji']} {cat['name']:22s} "
                f"{len(products):>3} productos | "
                f"top score 🇵🇦 {top['panama']['score']}/100"
            )
    print(f"{'='*55}\n")


async def main() -> None:
    now = datetime.utcnow()
    print(f"\n🚀 Iniciando Amazon Spy — {now.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"   Categorías: {len(CATEGORIES)}\n")

    # 1 — Scrape
    raw_results = await run_scraper(CATEGORIES)

    # 2 — Enrich
    cat_map = {c["id"]: c for c in CATEGORIES}
    all_products: dict[str, list[dict]] = {}
    for cat_id, products in raw_results.items():
        cat = cat_map[cat_id]
        all_products[cat_id] = enrich(products, cat)

    # 3 — Summary to stdout
    print_summary(all_products)

    # 4 — Generate HTML report
    REPORTS_DIR.mkdir(exist_ok=True)
    date_slug = now.strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"{date_slug}.html"
    latest_path = REPORTS_DIR / "latest.html"

    html = generate_html(all_products, CATEGORIES, now)
    report_path.write_text(html, encoding="utf-8")
    latest_path.write_text(html, encoding="utf-8")
    print(f"✅ Reporte generado: {report_path}")

    # 5 — Save JSON data (for future analysis)
    json_path = REPORTS_DIR / f"{date_slug}.json"
    json_path.write_text(
        json.dumps(all_products, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"✅ Datos JSON: {json_path}")
    print("\n🏁 Done.\n")


if __name__ == "__main__":
    asyncio.run(main())
