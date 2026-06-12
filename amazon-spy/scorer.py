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

    description = generate_panama_description(product, category, score)

    return {
        "score": score,
        "level": level,
        "emoji": emoji,
        "notes": category["panama_notes"],
        "description": description,
    }


_CAT_INSIGHTS = {
    "belleza": "Panamá tiene una cultura de belleza muy activa en redes — TikTok e Instagram impulsan ventas de estos productos todo el año.",
    "viaje": "Panamá como hub de tránsito internacional hace de los accesorios de viaje un nicho con demanda natural y constante.",
    "hogar": "Tendencias de organización del hogar son virales en TikTok Panamá — el contenido 'antes y después' convierte muy bien.",
    "mascotas": "El mercado de mascotas en Panamá crece aceleradamente. Los dueños panameños no escatiman en gastos para sus animales.",
    "fitness": "Cultura de gym muy arraigada en PtyCity. Productos de fitness con demos en video generan alta conversión en redes.",
    "bebe": "Alta tasa de natalidad y padres jóvenes digitalizados. Compra emocional — el precio no es barrera para la seguridad del bebé.",
    "tech": "Alta penetración de smartphones. Accesorios con diseño e identidad visual se diferencian fácilmente de los genéricos locales.",
}


def generate_panama_description(product: dict, category: dict, score: int) -> str:
    """Generate a product-specific Panama market description."""
    rank = product.get("rank", 50)
    reviews = product.get("reviews", 0)
    sales = product.get("monthly_sales_est", 0)
    price_raw = re.sub(r"[^\d.]", "", product.get("price", "0") or "0")
    try:
        price = float(price_raw)
    except ValueError:
        price = 0

    parts = []

    # Validation signal based on sales volume
    if sales >= 2000:
        parts.append(f"Producto muy validado con ~{sales:,} ventas/mes en Amazon USA.")
    elif sales >= 800:
        parts.append(f"Buen volumen con ~{sales:,} ventas/mes — señal de demanda real y sostenida.")
    else:
        parts.append(f"Volumen moderado de ~{sales:,} ventas/mes en USA.")

    # Competition signal based on reviews
    if reviews < 100:
        parts.append(
            "Muy pocas reseñas indica mercado poco saturado — gran oportunidad de ser primero en Panamá."
        )
    elif reviews < 500:
        parts.append(
            "Competencia media en USA. En Panamá hay espacio para posicionarse con buen branding local."
        )
    elif reviews < 2000:
        parts.append(
            "Mercado validado con competencia moderada. Diferenciación en diseño o packaging puede marcar la diferencia."
        )
    else:
        parts.append(
            f"Producto muy competido en USA ({reviews:,} reseñas). En Panamá el mercado es más pequeño y hay más espacio."
        )

    # Price signal
    if price < 15:
        parts.append("Precio muy bajo — ideal para primer pedido impulsivo online sin fricción.")
    elif price <= 35:
        parts.append("Precio accesible para clase media panameña — compra impulsiva viable en redes.")
    elif price <= 55:
        parts.append("Precio medio, requiere buena presentación y construir confianza de marca desde el inicio.")
    else:
        parts.append(
            f"Precio elevado (${price:.0f}). Segmento premium — mercado más reducido pero con mayor margen."
        )

    # Category-specific insight
    insight = _CAT_INSIGHTS.get(category["id"], "")
    if insight:
        parts.append(insight)

    return " ".join(parts)
