import re


def estimate_monthly_sales(rank: int) -> int:
    """Estimate monthly units sold based on Best Sellers page rank."""
    if rank <= 1:
        return 6000
    elif rank <= 3:
        return 3500
    elif rank <= 5:
        return 2200
    elif rank <= 10:
        return 1400
    elif rank <= 20:
        return 850
    elif rank <= 30:
        return 550
    elif rank <= 50:
        return 320
    elif rank <= 75:
        return 160
    else:
        return 80


def score_panama(product: dict, category: dict) -> dict:
    """Score a product's potential for Panama private label ecommerce."""
    score = category["panama_base"]

    # Price adjustment
    price_raw = re.sub(r"[^\d.]", "", product.get("price", "0") or "0")
    try:
        price = float(price_raw)
    except ValueError:
        price = 0

    if 15 <= price <= 35:
        score += 8
    elif 35 < price <= 55:
        score += 4
    elif 55 < price <= 80:
        score += 0
    elif price > 80:
        score -= 8
    else:
        score -= 4

    # Competition via reviews (fewer reviews = less saturated = opportunity)
    reviews = product.get("reviews", 0)
    if reviews < 100:
        score += 6
    elif reviews < 500:
        score += 3
    elif reviews < 2000:
        score += 0
    else:
        score -= 3

    # Rank on page (lower rank = more validated product)
    rank = product.get("rank", 50)
    if rank <= 5:
        score += 5
    elif rank <= 15:
        score += 2
    elif rank > 40:
        score -= 2

    # Quality signal from rating
    rating = product.get("rating", 0)
    if rating >= 4.5:
        score += 2
    elif rating < 3.8:
        score -= 4

    score = max(0, min(100, round(score)))

    if score >= 85:
        level, emoji = "ALTO", "🟢"
    elif score >= 70:
        level, emoji = "MEDIO", "🟡"
    else:
        level, emoji = "BAJO", "🔴"

    return {
        "score": score,
        "level": level,
        "emoji": emoji,
        "notes": category["panama_notes"],
    }
