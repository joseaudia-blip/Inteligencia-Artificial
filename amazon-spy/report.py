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
    price_num = _price_num(p.get("price", "0"))
    revenue_est = sales * price_num
    revenue_fmt = f"${revenue_est:,.0f}" if revenue_est else "—"
    reviews = p.get("reviews", 0)
    reviews_fmt = f"{reviews:,}"
    rating = p.get("rating", 0)
    stars = "★" * int(rating) + ("½" if rating % 1 >= 0.5 else "") if rating else "—"
    img = p.get("image", "")
    url = p.get("url", "#")
    title = p.get("title", "Sin título")[:80]
    price = p.get("price") or "—"
    rank = p.get("rank", "—")
    description = panama.get("description", "")

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

    <div class="sales-highlight">
      <div class="sales-item">
        <div class="sales-label">📈 Ventas est./mes (BSR)</div>
        <div class="sales-value">~{sales_fmt} uds</div>
      </div>
      <div class="sales-divider"></div>
      <div class="sales-item">
        <div class="sales-label">💵 Revenue est./mes</div>
        <div class="sales-value">{revenue_fmt}</div>
      </div>
    </div>

    <div class="panama-section">
      <div class="panama-header">
        <span>🇵🇦 Potencial Panamá</span>
        <span class="panama-score" style="color:{pcolor}">{panama['emoji']} {score}/100 — {panama['level']}</span>
      </div>
      {_score_bar(score, pcolor)}
      <div class="panama-description">
        <span class="desc-icon">💡</span>
        <span class="desc-text">{description}</span>
      </div>
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
<div class="summary-card" data-cat="{cat['id']}" style="border-top:3px solid {cat['color']};color:{cat['color']}" onclick="filterByCat('{cat['id']}')" role="button">
  <div class="sum-emoji">{cat['emoji']}</div>
  <div class="sum-name" style="color:#9ca3af">Sin datos</div>
</div>"""
    avg_score = round(sum(p["panama"]["score"] for p in products) / count)
    return f"""
<div class="summary-card" data-cat="{cat['id']}" style="border-top:3px solid {cat['color']};color:{cat['color']}" onclick="filterByCat('{cat['id']}')" role="button">
  <div class="sum-emoji">{cat['emoji']}</div>
  <div class="sum-name">{cat['name']}</div>
  <div class="sum-score">🇵🇦 {avg_score}/100</div>
</div>"""


def generate_email_html(
    all_products: dict[str, list[dict]],
    categories: list[dict],
    run_date: datetime,
) -> str:
    """Generate a simplified, email-client-compatible HTML (inline CSS, no JS)."""
    date_str = run_date.strftime("%A %d %b %Y")
    total = sum(len(v) for v in all_products.values())
    cat_map = {c["id"]: c for c in categories}

    flat = []
    for cat_id, products in all_products.items():
        for p in products:
            flat.append((p, cat_map[cat_id]))
    top10 = sorted(flat, key=lambda x: x[0]["panama"]["score"], reverse=True)[:10]

    rows = ""
    for i, (p, cat) in enumerate(top10, 1):
        score = p["panama"]["score"]
        pcolor = _panama_color(score)
        sales = p.get("monthly_sales_est", 0)
        price_n = _price_num(p.get("price", "0"))
        revenue = f"${sales * price_n:,.0f}" if price_n else "—"
        title = p.get("title", "")[:65]
        url = p.get("url", "#")
        img = p.get("image", "")
        price = p.get("price") or "—"
        rating = p.get("rating", 0)
        reviews = p.get("reviews", 0)
        desc = p["panama"].get("description", "")[:200]

        rows += f"""
<tr style="border-bottom:1px solid #e2e8f0;">
  <td style="padding:16px 8px;vertical-align:top;width:60px;text-align:center;">
    <div style="background:#1a1a2e;color:#fff;border-radius:50%;width:32px;height:32px;
                line-height:32px;font-weight:800;font-size:.8rem;margin:0 auto 8px;">
      {i}
    </div>
    {'<img src="' + img + '" width="56" height="56" style="object-fit:contain;border-radius:6px;background:#f8fafc;" alt="">' if img else ''}
  </td>
  <td style="padding:16px 8px;vertical-align:top;">
    <div style="font-size:.7rem;font-weight:700;color:{cat['color']};margin-bottom:4px;">
      {cat['emoji']} {cat['name']}
    </div>
    <a href="{url}" style="font-size:.85rem;font-weight:600;color:#1a1a2e;text-decoration:none;line-height:1.4;display:block;margin-bottom:6px;">
      {title}…
    </a>
    <table cellpadding="0" cellspacing="0" style="width:100%;margin-bottom:8px;">
      <tr>
        <td style="font-size:.75rem;color:#6b7280;">Precio</td>
        <td style="font-size:.75rem;color:#6b7280;">Rating</td>
        <td style="font-size:.75rem;color:#6b7280;">Reseñas</td>
      </tr>
      <tr>
        <td style="font-size:.85rem;font-weight:700;color:#b12704;">{price}</td>
        <td style="font-size:.85rem;font-weight:600;">⭐ {rating}</td>
        <td style="font-size:.85rem;font-weight:600;">{reviews:,}</td>
      </tr>
    </table>
    <table cellpadding="0" cellspacing="6" style="background:#eff6ff;border-radius:8px;
           padding:8px;width:100%;margin-bottom:8px;">
      <tr>
        <td style="font-size:.68rem;color:#6b7280;font-weight:500;">📈 Ventas est./mes</td>
        <td style="font-size:.68rem;color:#6b7280;font-weight:500;">💵 Revenue est./mes</td>
      </tr>
      <tr>
        <td style="font-size:.9rem;font-weight:800;color:#1e40af;">~{sales:,} uds</td>
        <td style="font-size:.9rem;font-weight:800;color:#1e40af;">{revenue}</td>
      </tr>
    </table>
    <table cellpadding="0" cellspacing="0" style="width:100%;margin-bottom:6px;">
      <tr>
        <td style="font-size:.75rem;font-weight:600;color:#374151;">🇵🇦 Potencial Panamá</td>
        <td align="right" style="font-size:.75rem;font-weight:700;color:{pcolor};">
          {p['panama']['emoji']} {score}/100 — {p['panama']['level']}
        </td>
      </tr>
    </table>
    <div style="background:#e2e8f0;border-radius:99px;height:5px;margin-bottom:8px;">
      <div style="background:{pcolor};width:{score}%;height:5px;border-radius:99px;"></div>
    </div>
    <div style="background:#fff;border-left:3px solid #94a3b8;border-radius:4px;
                padding:7px 9px;font-size:.7rem;color:#374151;line-height:1.5;">
      💡 {desc}
    </div>
    <a href="{url}" style="display:inline-block;margin-top:8px;background:#1565c0;
       color:#fff;border-radius:6px;padding:6px 14px;font-size:.75rem;
       font-weight:600;text-decoration:none;">Ver en Amazon →</a>
  </td>
</tr>"""

    cat_summary = ""
    for cat in categories:
        prods = all_products.get(cat["id"], [])
        count = len(prods)
        avg = round(sum(p["panama"]["score"] for p in prods) / count) if prods else 0
        cat_summary += f"""
<td style="text-align:center;padding:8px 6px;vertical-align:top;">
  <div style="font-size:1.4rem;">{cat['emoji']}</div>
  <div style="font-size:.68rem;color:#6b7280;font-weight:600;margin:3px 0;">{cat['name']}</div>
  <div style="font-size:.85rem;font-weight:700;color:{cat['color']};">{count} prods</div>
  <div style="font-size:.68rem;color:#6b7280;">🇵🇦 {avg}/100</div>
</td>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🔥 Trending Amazon Panamá — {date_str}</title></head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
<table cellpadding="0" cellspacing="0" width="100%" style="max-width:620px;margin:0 auto;">
  <tr><td>

    <!-- HEADER -->
    <table cellpadding="0" cellspacing="0" width="100%"
           style="background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:12px 12px 0 0;margin-top:16px;">
      <tr><td style="padding:28px 24px;text-align:center;">
        <div style="font-size:1.4rem;font-weight:800;color:#fff;letter-spacing:-.5px;">
          🔥 Trending Amazon — Panamá
        </div>
        <div style="font-size:.85rem;color:#94a3b8;margin-top:6px;">
          🗓️ {date_str} · ⏰ 06:00 AM · Movers &amp; Shakers — productos que más suben hoy
        </div>
        <table cellpadding="0" cellspacing="8" style="margin:14px auto 0;">
          <tr>
            <td style="background:rgba(255,255,255,.1);border-radius:99px;padding:5px 14px;
                        font-size:.78rem;font-weight:600;color:#fff;">🔍 7 categorías</td>
            <td style="background:rgba(255,255,255,.1);border-radius:99px;padding:5px 14px;
                        font-size:.78rem;font-weight:600;color:#fff;">📦 {total} productos</td>
            <td style="background:rgba(255,255,255,.1);border-radius:99px;padding:5px 14px;
                        font-size:.78rem;font-weight:600;color:#fff;">🇵🇦 Mercado Panamá</td>
          </tr>
        </table>
      </td></tr>
    </table>

    <!-- RESUMEN CATEGORÍAS -->
    <table cellpadding="0" cellspacing="0" width="100%"
           style="background:#fff;padding:16px;">
      <tr><td colspan="7" style="font-size:.9rem;font-weight:700;padding-bottom:12px;">
        📊 Resumen por categoría
      </td></tr>
      <tr>{cat_summary}</tr>
    </table>

    <!-- TOP 10 -->
    <table cellpadding="0" cellspacing="0" width="100%"
           style="background:#fff;border-top:1px solid #e2e8f0;">
      <tr><td colspan="2" style="padding:16px 16px 4px;font-size:.9rem;font-weight:700;">
        🏆 Top 10 del día — Mayor potencial en Panamá
      </td></tr>
      {rows}
    </table>

    <!-- FOOTER -->
    <table cellpadding="0" cellspacing="0" width="100%"
           style="background:#f8fafc;border-radius:0 0 12px 12px;border-top:1px solid #e2e8f0;">
      <tr><td style="padding:14px;text-align:center;font-size:.72rem;color:#9ca3af;">
        Generado automáticamente · Amazon USA Movers &amp; Shakers · {date_str}<br>
        El reporte interactivo completo está adjunto (reporte.html)
      </td></tr>
    </table>

  </td></tr>
</table>
</body></html>"""


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
    buttons_html = (
        '<button class="filter-btn active" data-cat="all" '
        'onclick="filterCat(this,\'all\')">📊 Todas ({n})</button>'
    ).format(n=total_products)
    for cat in categories:
        count = len(all_products.get(cat["id"], []))
        buttons_html += (
            f'<button class="filter-btn" data-cat="{cat["id"]}" '
            f'onclick="filterCat(this,\'{cat["id"]}\')" '
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
<title>🔥 Trending Amazon Panamá — {date_str}</title>
<meta name="theme-color" content="#1a1a2e">
<style>
  :root {{
    --radius: 14px;
    --shadow: 0 2px 12px rgba(0,0,0,.08);
    --bg: #f0f2f5;
    --surface: #fff;
    --text: #1a1a2e;
    --muted: #6b7280;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
  body {{ font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
          background: var(--bg); color: var(--text); font-size: 16px; }}

  /* ── HEADER ─────────────────────────────────── */
  .header {{ background: linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);
             color: #fff; padding: 24px 20px 20px; text-align: center; }}
  .header h1 {{ font-size: clamp(1.1rem,4vw,1.6rem); font-weight: 800;
                letter-spacing: -.5px; line-height: 1.2; }}
  .header-sub {{ color: #94a3b8; font-size: .85rem; margin-top: 6px; }}
  .header-stats {{ display: flex; justify-content: center; gap: 8px;
                   margin-top: 14px; flex-wrap: wrap; }}
  .stat-pill {{ background: rgba(255,255,255,.12); border-radius: 999px;
                padding: 6px 14px; font-size: .8rem; font-weight: 600; }}

  /* ── SECTIONS ────────────────────────────────── */
  .section {{ max-width: 1300px; margin: 20px auto; padding: 0 12px; }}
  .section-title {{ font-size: 1rem; font-weight: 700; margin-bottom: 14px;
                    display: flex; align-items: center; gap: 8px; }}

  /* ── SUMMARY GRID ────────────────────────────── */
  .summary-grid {{ display: grid;
                   grid-template-columns: repeat(auto-fill,minmax(110px,1fr));
                   gap: 10px; }}
  .summary-card {{ background: var(--surface); border-radius: var(--radius);
                   padding: 12px 10px; box-shadow: var(--shadow);
                   cursor: pointer; transition: transform .15s, box-shadow .15s;
                   text-align: center; }}
  .summary-card:hover, .summary-card:active {{ transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0,0,0,.14); }}
  .summary-card.active-filter {{ outline: 2.5px solid; }}
  .sum-emoji {{ font-size: 1.6rem; }}
  .sum-name {{ font-size: .75rem; font-weight: 700; margin: 5px 0 3px;
               color: var(--text); line-height: 1.3; }}
  .sum-score {{ font-size: .68rem; color: var(--muted); }}
  .sum-top {{ display: none; }}

  /* ── STICKY FILTER BAR ───────────────────────── */
  .filter-bar-wrap {{ position: sticky; top: 0; z-index: 100;
                      background: var(--surface);
                      border-bottom: 1px solid #e2e8f0;
                      box-shadow: 0 2px 8px rgba(0,0,0,.07); }}
  .filter-bar {{ max-width: 1300px; margin: 0 auto;
                 display: flex; gap: 8px; padding: 10px 12px;
                 overflow-x: auto; -webkit-overflow-scrolling: touch;
                 scrollbar-width: none; }}
  .filter-bar::-webkit-scrollbar {{ display: none; }}
  .filter-btn {{ flex-shrink: 0; background: var(--bg);
                 border: 1.5px solid #e2e8f0; border-radius: 999px;
                 padding: 10px 16px; font-size: .8rem; font-weight: 600;
                 cursor: pointer; transition: all .18s; color: var(--text);
                 min-height: 44px; white-space: nowrap; }}
  .filter-btn.active {{ background: var(--cat-color,#1565c0);
                        border-color: var(--cat-color,#1565c0); color: #fff; }}

  /* ── PRODUCT GRID ────────────────────────────── */
  .products-grid {{ max-width: 1300px; margin: 0 auto;
                    padding: 12px 12px 48px;
                    display: grid;
                    grid-template-columns: repeat(auto-fill,minmax(300px,1fr));
                    gap: 14px; }}

  /* ── PRODUCT CARD ────────────────────────────── */
  .product-card {{ background: var(--surface); border-radius: var(--radius);
                   box-shadow: var(--shadow); overflow: hidden;
                   display: flex; flex-direction: column; position: relative; }}
  .card-rank {{ position: absolute; top: 10px; left: 10px;
                background: #1a1a2e; color: #fff; border-radius: 999px;
                font-size: .72rem; font-weight: 700; padding: 3px 10px; z-index: 2; }}
  .card-image-wrap {{ height: 190px; background: #f8fafc; display: flex;
                      align-items: center; justify-content: center; overflow: hidden; }}
  .card-image {{ width: 100%; height: 100%; object-fit: contain; padding: 14px; }}
  .card-image-placeholder {{ font-size: 3rem; }}
  .card-body {{ padding: 14px 14px 16px; display: flex;
                flex-direction: column; gap: 10px; flex: 1; }}
  .card-cat-badge {{ font-size: .7rem; font-weight: 700; border-radius: 999px;
                     padding: 3px 10px; display: inline-block; width: fit-content; }}
  .card-title {{ font-size: .9rem; font-weight: 600; color: var(--text);
                 text-decoration: none; line-height: 1.45;
                 display: -webkit-box; -webkit-line-clamp: 2;
                 -webkit-box-orient: vertical; overflow: hidden; }}
  .card-meta {{ display: flex; flex-direction: column; gap: 3px; }}
  .meta-price {{ font-size: 1.1rem; font-weight: 700; color: #b12704; }}
  .meta-rating {{ font-size: .82rem; color: var(--muted); }}

  /* ── SALES HIGHLIGHT BOX ─────────────────────── */
  .sales-highlight {{ display: flex; background: #eff6ff;
                      border: 1px solid #bfdbfe; border-radius: 10px;
                      overflow: hidden; }}
  .sales-item {{ flex: 1; padding: 11px 12px; display: flex;
                 flex-direction: column; gap: 2px; }}
  .sales-label {{ font-size: .68rem; color: #6b7280; font-weight: 500; }}
  .sales-value {{ font-size: 1.05rem; font-weight: 800; color: #1e40af; }}
  .sales-divider {{ width: 1px; background: #bfdbfe; margin: 8px 0; }}

  /* ── PANAMA SECTION ──────────────────────────── */
  .panama-section {{ background: #f8fafc; border-radius: 10px; padding: 12px; }}
  .panama-header {{ display: flex; justify-content: space-between;
                    align-items: center; font-size: .8rem; font-weight: 700;
                    margin-bottom: 7px; }}
  .panama-score {{ font-size: .78rem; font-weight: 700; }}
  .score-bar-wrap {{ background: #e2e8f0; border-radius: 999px; height: 8px;
                     overflow: hidden; margin-bottom: 10px; }}
  .score-bar-fill {{ height: 100%; border-radius: 999px; }}
  .panama-description {{ display: flex; gap: 6px; align-items: flex-start;
                          background: #fff; border-radius: 7px; padding: 9px 10px;
                          border-left: 3px solid #94a3b8; }}
  .desc-icon {{ font-size: .85rem; flex-shrink: 0; margin-top: 1px; }}
  .desc-text {{ font-size: .75rem; color: #374151; line-height: 1.55; }}

  /* ── VIEW BUTTON ─────────────────────────────── */
  .view-btn {{ display: block; text-align: center; background: #1565c0;
               color: #fff !important; border-radius: 10px; padding: 13px;
               text-decoration: none; font-size: .88rem; font-weight: 700;
               margin-top: 4px; letter-spacing: .2px; }}

  /* ── TOP 5 GRID ──────────────────────────────── */
  .top5-grid {{ display: grid;
                grid-template-columns: repeat(auto-fill,minmax(280px,1fr));
                gap: 14px; }}

  /* ── FOOTER ──────────────────────────────────── */
  .footer {{ text-align: center; padding: 20px 16px 40px;
             font-size: .75rem; color: var(--muted); line-height: 1.6; }}

  /* ══ MOBILE OVERRIDES (≤ 640px) ════════════════ */
  @media (max-width: 640px) {{
    .header {{ padding: 20px 16px 16px; }}
    .section {{ padding: 0 10px; }}
    .summary-grid {{ grid-template-columns: repeat(4,1fr); gap: 8px; }}
    .sum-name {{ font-size: .65rem; }}
    .products-grid {{ grid-template-columns: 1fr; padding: 10px 10px 60px; gap: 12px; }}
    .top5-grid {{ grid-template-columns: 1fr; }}
    .card-image-wrap {{ height: 170px; }}
    .card-body {{ padding: 12px 12px 14px; }}
    .card-title {{ font-size: .88rem; }}
    .meta-price {{ font-size: 1.05rem; }}
    .sales-value {{ font-size: 1rem; }}
    .view-btn {{ padding: 14px; font-size: .92rem; }}
    .filter-btn {{ padding: 10px 14px; font-size: .78rem; }}
    .score-bar-wrap {{ height: 9px; }}
  }}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <h1>🔥 Trending Amazon — Panamá</h1>
  <div class="header-sub">🗓️ {date_str} · ⏰ {time_str} · Movers &amp; Shakers — productos que más suben hoy</div>
  <div class="header-stats">
    <span class="stat-pill">🔍 7 categorías</span>
    <span class="stat-pill">📦 {total_products} productos</span>
    <span class="stat-pill">🇵🇦 Mercado Panamá</span>
  </div>
</div>

<!-- FILTROS (sticky — justo bajo el header) -->
<div class="filter-bar-wrap">
  <div class="filter-bar">
    {buttons_html}
  </div>
</div>

<!-- RESUMEN POR CATEGORÍA -->
<div class="section">
  <div class="section-title">📊 Toca una categoría para filtrar</div>
  <div class="summary-grid">
    {summary_html}
  </div>
</div>

<!-- TOP 5 DEL DÍA -->
<div class="section" id="top5-section">
  <div class="section-title">🏆 Top 5 del día — Mayor potencial en Panamá</div>
  <div class="top5-grid">
    {top5_html}
  </div>
</div>

<!-- TODOS LOS PRODUCTOS -->
<div class="products-grid" id="products-grid">
  {all_cards_html}
</div>

<div class="footer">
  Generado automáticamente · Amazon USA Movers &amp; Shakers · {date_str}
</div>

<script>
  function applyFilter(cat) {{
    // Filter bar buttons
    document.querySelectorAll('.filter-btn').forEach(b => {{
      b.classList.toggle('active', b.getAttribute('data-cat') === cat);
    }});
    // Summary cards — hide the ones NOT selected (show all when "all")
    document.querySelectorAll('.summary-card').forEach(c => {{
      const match = cat === 'all' || c.getAttribute('data-cat') === cat;
      c.style.display = match ? '' : 'none';
      c.classList.toggle('active-filter', cat !== 'all' && match);
    }});
    // Top 5 section — hide when filtering a category (mixed results confuse)
    var top5 = document.getElementById('top5-section');
    if (top5) top5.style.display = cat === 'all' ? '' : 'none';
    // Product cards — show only selected category
    document.querySelectorAll('#products-grid .product-card').forEach(card => {{
      card.style.display = (cat === 'all' || card.dataset.category === cat) ? '' : 'none';
    }});
  }}

  function filterCat(btn, cat) {{ applyFilter(cat); }}
  function filterByCat(cat) {{ applyFilter(cat); }}
</script>
</body>
</html>"""
