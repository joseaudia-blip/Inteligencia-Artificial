from datetime import datetime


def _score_bar(score: int, color: str) -> str:
    pct = max(0, min(100, score))
    return (
        f'<div class="score-bar-wrap">'
        f'<div class="score-bar-fill" style="width:{pct}%;background:{color}"></div>'
        f'</div>'
    )


def _panama_color(score: int) -> str:
    if score >= 85:
        return "#2e7d32"
    if score >= 70:
        return "#e65100"
    return "#c62828"


def _product_card(p: dict, cat: dict) -> str:
    panama = p["panama"]
    score = panama["score"]
    pcolor = _panama_color(score)
    sales = p.get("monthly_sales_est", 0)
    sales_fmt = f"{sales:,}"
    revenue_est = sales * _price_num(p.get("price", "0"))
    revenue_fmt = f"${revenue_est:,.0f}" if revenue_est else "—"
    reviews_fmt = f"{p.get('reviews', 0):,}"
    rating = p.get("rating", 0)
    stars = "★" * int(rating) + ("½" if rating % 1 >= 0.5 else "") if rating else "—"
    img = p.get("image", "")
    url = p.get("url", "#")
    title = p.get("title", "Sin título")[:80]
    price = p.get("price") or "—"
    rank = p.get("rank", "—")

    return f"""
<div class="product-card" data-category="{cat['id']}" data-score="{score}">
  <div class="card-rank">#{rank}</div>
  <div class="card-image-wrap">
    {'<img class="card-image" src="' + img + '" alt="product" loading="lazy">' if img else '<div class="card-image-placeholder">📦</div>'}
  </div>
  <div class="card-body">
    <div class="card-cat-badge" style="background:{cat['color']}20;color:{cat['color']}">
      {cat['emoji']} {cat['name']}
    </div>
    <a class="card-title" href="{url}" target="_blank" rel="noopener">{title}</a>
    <div class="card-meta">
      <span class="meta-price">{price}</span>
      <span class="meta-rating">{stars} <small>({reviews_fmt} reseñas)</small></span>
    </div>
    <div class="card-sales">
      <span>📈 ~{sales_fmt} uds/mes</span>
      <span>💵 Revenue ~{revenue_fmt}/mes</span>
    </div>
    <div class="panama-section">
      <div class="panama-header">
        <span>🇵🇦 Potencial Panamá</span>
        <span class="panama-score" style="color:{pcolor}">{panama['emoji']} {score}/100 — {panama['level']}</span>
      </div>
      {_score_bar(score, pcolor)}
      <div class="panama-notes">{panama['notes']}</div>
    </div>
    <a class="view-btn" href="{url}" target="_blank" rel="noopener">Ver en Amazon →</a>
  </div>
</div>"""


def _price_num(price_str: str) -> float:
    import re
    raw = re.sub(r"[^\d.]", "", price_str or "0")
    try:
        return float(raw)
    except ValueError:
        return 0.0


def _category_summary_card(cat: dict, products: list[dict]) -> str:
    count = len(products)
    if not products:
        return f"""
<div class="summary-card" style="border-top:3px solid {cat['color']}">
  <div class="sum-emoji">{cat['emoji']}</div>
  <div class="sum-name">{cat['name']}</div>
  <div class="sum-count">Sin datos</div>
</div>"""
    avg_score = round(sum(p["panama"]["score"] for p in products) / count)
    top = products[0]
    return f"""
<div class="summary-card" style="border-top:3px solid {cat['color']}">
  <div class="sum-emoji">{cat['emoji']}</div>
  <div class="sum-name">{cat['name']}</div>
  <div class="sum-count" style="color:{cat['color']}">{count} productos</div>
  <div class="sum-score">🇵🇦 Avg {avg_score}/100</div>
  <div class="sum-top">🏆 #{top['rank']} {top['title'][:35]}…</div>
</div>"""


def generate_html(
    all_products: dict[str, list[dict]],
    categories: list[dict],
    run_date: datetime,
) -> str:
    total_products = sum(len(v) for v in all_products.values())
    date_str = run_date.strftime("%A %d %b %Y")
    time_str = run_date.strftime("%H:%M")

    # Top 5 overall by Panama score
    flat = []
    cat_map = {c["id"]: c for c in categories}
    for cat_id, products in all_products.items():
        cat = cat_map[cat_id]
        for p in products:
            flat.append((p, cat))
    top5 = sorted(flat, key=lambda x: x[0]["panama"]["score"], reverse=True)[:5]

    # Filter buttons HTML
    buttons_html = '<button class="filter-btn active" onclick="filterCat(this,\'all\')">📊 Todas ({n})</button>'.format(
        n=total_products
    )
    for cat in categories:
        count = len(all_products.get(cat["id"], []))
        buttons_html += (
            f'<button class="filter-btn" onclick="filterCat(this,\'{cat["id"]}\')" '
            f'style="--cat-color:{cat["color"]}">'
            f'{cat["emoji"]} {cat["name"]} ({count})</button>'
        )

    # Summary cards
    summary_html = "".join(
        _category_summary_card(cat, all_products.get(cat["id"], []))
        for cat in categories
    )

    # Top 5 cards
    top5_html = "".join(_product_card(p, c) for p, c in top5)

    # All product cards
    all_cards_html = ""
    for cat in categories:
        for p in all_products.get(cat["id"], []):
            all_cards_html += _product_card(p, cat)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Amazon Spy — {date_str}</title>
<style>
  :root {{
    --radius: 12px;
    --shadow: 0 2px 12px rgba(0,0,0,.08);
    --bg: #f4f6f9;
    --surface: #fff;
    --text: #1a1a2e;
    --muted: #6b7280;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
          background: var(--bg); color: var(--text); }}

  /* HEADER */
  .header {{ background: linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);
             color: #fff; padding: 28px 24px 22px; text-align: center; }}
  .header h1 {{ font-size: 1.6rem; font-weight: 700; letter-spacing: -.5px; }}
  .header-sub {{ color: #94a3b8; font-size: .9rem; margin-top: 6px; }}
  .header-stats {{ display: flex; justify-content: center; gap: 24px;
                   margin-top: 16px; flex-wrap: wrap; }}
  .stat-pill {{ background: rgba(255,255,255,.1); border-radius: 999px;
                padding: 6px 16px; font-size: .85rem; font-weight: 600; }}

  /* SECTION TITLES */
  .section {{ max-width: 1300px; margin: 28px auto; padding: 0 16px; }}
  .section-title {{ font-size: 1.15rem; font-weight: 700; margin-bottom: 16px;
                    display: flex; align-items: center; gap: 8px; }}

  /* SUMMARY CARDS */
  .summary-grid {{ display: grid;
                   grid-template-columns: repeat(auto-fill,minmax(170px,1fr));
                   gap: 12px; }}
  .summary-card {{ background: var(--surface); border-radius: var(--radius);
                   padding: 16px 14px; box-shadow: var(--shadow); }}
  .sum-emoji {{ font-size: 1.6rem; }}
  .sum-name {{ font-size: .8rem; color: var(--muted); margin: 4px 0 2px; font-weight: 600; }}
  .sum-count {{ font-size: 1.1rem; font-weight: 700; }}
  .sum-score {{ font-size: .78rem; color: var(--muted); margin-top: 4px; }}
  .sum-top {{ font-size: .72rem; color: var(--muted); margin-top: 4px;
              white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}

  /* FILTER BAR */
  .filter-bar {{ max-width: 1300px; margin: 0 auto 20px; padding: 0 16px;
                  display: flex; flex-wrap: wrap; gap: 8px; }}
  .filter-btn {{ background: var(--surface); border: 1.5px solid #e2e8f0;
                 border-radius: 999px; padding: 7px 16px; font-size: .82rem;
                 font-weight: 600; cursor: pointer; transition: all .18s;
                 color: var(--text); }}
  .filter-btn:hover {{ border-color: var(--cat-color,#1565c0);
                       color: var(--cat-color,#1565c0); }}
  .filter-btn.active {{ background: var(--cat-color,#1565c0);
                        border-color: var(--cat-color,#1565c0);
                        color: #fff; }}

  /* PRODUCT GRID */
  .products-grid {{ max-width: 1300px; margin: 0 auto; padding: 0 16px 40px;
                    display: grid;
                    grid-template-columns: repeat(auto-fill,minmax(300px,1fr));
                    gap: 18px; }}
  .product-card {{ background: var(--surface); border-radius: var(--radius);
                   box-shadow: var(--shadow); overflow: hidden;
                   display: flex; flex-direction: column; position: relative;
                   transition: transform .2s, box-shadow .2s; }}
  .product-card:hover {{ transform: translateY(-3px);
                         box-shadow: 0 8px 24px rgba(0,0,0,.12); }}
  .card-rank {{ position: absolute; top: 10px; left: 10px; background: #1a1a2e;
                color: #fff; border-radius: 999px; font-size: .72rem;
                font-weight: 700; padding: 3px 10px; z-index: 2; }}
  .card-image-wrap {{ height: 200px; background: #f8fafc; display: flex;
                      align-items: center; justify-content: center; overflow: hidden; }}
  .card-image {{ width: 100%; height: 100%; object-fit: contain; padding: 12px; }}
  .card-image-placeholder {{ font-size: 3rem; }}
  .card-body {{ padding: 14px 16px 18px; display: flex; flex-direction: column; gap: 10px; }}
  .card-cat-badge {{ font-size: .72rem; font-weight: 700; border-radius: 999px;
                     padding: 3px 10px; display: inline-block; width: fit-content; }}
  .card-title {{ font-size: .88rem; font-weight: 600; color: var(--text);
                 text-decoration: none; line-height: 1.45;
                 display: -webkit-box; -webkit-line-clamp: 2;
                 -webkit-box-orient: vertical; overflow: hidden; }}
  .card-title:hover {{ color: #1565c0; }}
  .card-meta {{ display: flex; flex-direction: column; gap: 3px; }}
  .meta-price {{ font-size: 1.05rem; font-weight: 700; color: #b12704; }}
  .meta-rating {{ font-size: .8rem; color: var(--muted); }}
  .card-sales {{ display: flex; flex-direction: column; gap: 3px;
                 font-size: .8rem; color: #374151; font-weight: 500; }}
  .panama-section {{ background: #f8fafc; border-radius: 8px; padding: 12px; }}
  .panama-header {{ display: flex; justify-content: space-between;
                    align-items: center; font-size: .8rem; font-weight: 600;
                    margin-bottom: 6px; }}
  .panama-score {{ font-size: .78rem; }}
  .score-bar-wrap {{ background: #e2e8f0; border-radius: 999px; height: 6px;
                     overflow: hidden; margin-bottom: 7px; }}
  .score-bar-fill {{ height: 100%; border-radius: 999px; transition: width .4s; }}
  .panama-notes {{ font-size: .72rem; color: var(--muted); line-height: 1.4; }}
  .view-btn {{ display: block; text-align: center; background: #1565c0;
               color: #fff; border-radius: 8px; padding: 9px;
               text-decoration: none; font-size: .82rem; font-weight: 600;
               margin-top: 4px; transition: background .18s; }}
  .view-btn:hover {{ background: #0d47a1; }}

  /* TOP 5 section */
  .top5-grid {{ display: grid;
                grid-template-columns: repeat(auto-fill,minmax(280px,1fr));
                gap: 18px; }}

  /* FOOTER */
  .footer {{ text-align: center; padding: 20px; font-size: .78rem;
             color: var(--muted); }}

  @media (max-width: 600px) {{
    .header h1 {{ font-size: 1.2rem; }}
    .products-grid {{ grid-template-columns: 1fr; }}
    .top5-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <h1>📦 Amazon Fashion Spy — Panamá</h1>
  <div class="header-sub">🗓️ {date_str} · ⏰ {time_str} · Amazon USA</div>
  <div class="header-stats">
    <span class="stat-pill">🔍 7 categorías</span>
    <span class="stat-pill">📦 {total_products} productos</span>
    <span class="stat-pill">🇵🇦 Mercado Panamá</span>
  </div>
</div>

<!-- RESUMEN POR CATEGORÍA -->
<div class="section">
  <div class="section-title">📊 Resumen por categoría</div>
  <div class="summary-grid">
    {summary_html}
  </div>
</div>

<!-- TOP 5 DEL DÍA -->
<div class="section">
  <div class="section-title">🏆 Top 5 del día — Mayor potencial en Panamá</div>
  <div class="top5-grid">
    {top5_html}
  </div>
</div>

<!-- FILTROS -->
<div class="filter-bar">
  {buttons_html}
</div>

<!-- TODOS LOS PRODUCTOS -->
<div class="products-grid" id="products-grid">
  {all_cards_html}
</div>

<div class="footer">
  Generado automáticamente · Amazon USA Best Sellers · {date_str}
</div>

<script>
  function filterCat(btn, cat) {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('#products-grid .product-card').forEach(card => {{
      card.style.display = (cat === 'all' || card.dataset.category === cat) ? '' : 'none';
    }});
  }}
</script>
</body>
</html>"""
