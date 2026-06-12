"""Generate a demo HTML report with realistic mock data."""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from categories import CATEGORIES
from scorer import score_panama, estimate_monthly_sales
from report import generate_html

MOCK_DATA = {
    "belleza": [
        {"rank": 1, "asin": "B0CX1A", "title": "VELEASHA Makeup Brush Set 18 Pcs — Premium Synthetic Kabuki Foundation Blending Brushes", "image": "https://m.media-amazon.com/images/I/71zLiJVf+QL._AC_SL1500_.jpg", "price": "$18.99", "rating": 4.6, "reviews": 12847, "url": "https://www.amazon.com/dp/B0CX1A"},
        {"rank": 2, "asin": "B0CX2B", "title": "Jade Roller and Gua Sha Set — Face Roller Skin Care Tool for Anti-Aging Facial Massage", "image": "https://m.media-amazon.com/images/I/71ZfP5PMAQL._AC_SL1500_.jpg", "price": "$12.99", "rating": 4.4, "reviews": 8234, "url": "https://www.amazon.com/dp/B0CX2B"},
        {"rank": 3, "asin": "B0CX3C", "title": "BEAKEY Silicone Makeup Sponge Set 5 Pcs — Flawless Liquid Powder Foundation Blender", "image": "https://m.media-amazon.com/images/I/61j0TL3OkbL._AC_SL1500_.jpg", "price": "$9.99", "rating": 4.5, "reviews": 3421, "url": "https://www.amazon.com/dp/B0CX3C"},
        {"rank": 5, "asin": "B0CX4D", "title": "Eyelash Curler with 2 Refill Pads — Professional Eye Lash Curler for Natural Long Lasting Curl", "image": "https://m.media-amazon.com/images/I/51Fua7P0TZL._AC_SL1500_.jpg", "price": "$7.49", "rating": 4.3, "reviews": 567, "url": "https://www.amazon.com/dp/B0CX4D"},
        {"rank": 8, "asin": "B0CX5E", "title": "YANIBEST Silk Scrunchies Hair Ties 20 Pack — No Crease Satin Hair Ribbon for Women", "image": "https://m.media-amazon.com/images/I/71R0TG0QBSL._AC_SL1500_.jpg", "price": "$14.99", "rating": 4.7, "reviews": 89, "url": "https://www.amazon.com/dp/B0CX5E"},
    ],
    "viaje": [
        {"rank": 1, "asin": "B0VJ1A", "title": "BAGSMART Packing Cubes for Suitcase 8 Set — Travel Cube Organizer Luggage Compression", "image": "https://m.media-amazon.com/images/I/81YDcMD-QBL._AC_SL1500_.jpg", "price": "$29.99", "rating": 4.7, "reviews": 22341, "url": "https://www.amazon.com/dp/B0VJ1A"},
        {"rank": 2, "asin": "B0VJ2B", "title": "Waterproof Passport Holder Travel Wallet — RFID Blocking Document Organizer for Men Women", "image": "https://m.media-amazon.com/images/I/71sj1s6BXFL._AC_SL1500_.jpg", "price": "$19.99", "rating": 4.5, "reviews": 9876, "url": "https://www.amazon.com/dp/B0VJ2B"},
        {"rank": 4, "asin": "B0VJ3C", "title": "Luggage Scale Digital — 110 lbs Portable Electronic Baggage Scale with Backlit LCD Display", "image": "https://m.media-amazon.com/images/I/61-zK4K2OWL._AC_SL1500_.jpg", "price": "$11.99", "rating": 4.4, "reviews": 4532, "url": "https://www.amazon.com/dp/B0VJ3C"},
        {"rank": 7, "asin": "B0VJ4D", "title": "Travel Jewelry Organizer Case — Portable Jewelry Roll Bag with Mirror for Rings Earrings Necklaces", "image": "https://m.media-amazon.com/images/I/71eoPsJK1dL._AC_SL1500_.jpg", "price": "$16.99", "rating": 4.6, "reviews": 312, "url": "https://www.amazon.com/dp/B0VJ4D"},
        {"rank": 11, "asin": "B0VJ5E", "title": "YAMIU Toiletry Bag Hanging Travel Organizer — Waterproof Dopp Kit Cosmetic Bag for Men Women", "image": "https://m.media-amazon.com/images/I/71fwWtqZ5QL._AC_SL1500_.jpg", "price": "$22.99", "rating": 4.5, "reviews": 78, "url": "https://www.amazon.com/dp/B0VJ5E"},
    ],
    "hogar": [
        {"rank": 1, "asin": "B0HG1A", "title": "Stackable Storage Bins with Lids 6 Pack — Clear Plastic Organizer Boxes for Pantry Closet Shelf", "image": "https://m.media-amazon.com/images/I/81qRzCrAbnL._AC_SL1500_.jpg", "price": "$34.99", "rating": 4.6, "reviews": 18923, "url": "https://www.amazon.com/dp/B0HG1A"},
        {"rank": 3, "asin": "B0HG2B", "title": "Bamboo Drawer Organizer Dividers Set of 8 — Expandable Kitchen Utensil Organizer for Bedroom", "image": "https://m.media-amazon.com/images/I/71-5iG6CXWL._AC_SL1500_.jpg", "price": "$26.99", "rating": 4.5, "reviews": 7654, "url": "https://www.amazon.com/dp/B0HG2B"},
        {"rank": 5, "asin": "B0HG3C", "title": "Over The Door Organizer 8 Pockets — Large Clear Hanging Pantry Organizer for Bedroom Bathroom", "image": "https://m.media-amazon.com/images/I/61tU3PB-9JL._AC_SL1500_.jpg", "price": "$21.99", "rating": 4.4, "reviews": 3210, "url": "https://www.amazon.com/dp/B0HG3C"},
        {"rank": 9, "asin": "B0HG4D", "title": "Acrylic Makeup Organizer Display Case — Clear Cosmetic Storage for Lipstick Brushes Perfume", "image": "https://m.media-amazon.com/images/I/71nEF9OYDQL._AC_SL1500_.jpg", "price": "$27.99", "rating": 4.7, "reviews": 145, "url": "https://www.amazon.com/dp/B0HG4D"},
        {"rank": 14, "asin": "B0HG5E", "title": "Cable Management Box — Cord Organizer Desktop Wire Cover Hider for TV Power Strip", "image": "https://m.media-amazon.com/images/I/71c3KWVD2DL._AC_SL1500_.jpg", "price": "$18.99", "rating": 4.3, "reviews": 56, "url": "https://www.amazon.com/dp/B0HG5E"},
    ],
    "mascotas": [
        {"rank": 2, "asin": "B0PT1A", "title": "COMSUN Collapsible Dog Bowl Travel Set 4 Pack — Portable Silicone Food Water Bowl for Dogs Cats", "image": "https://m.media-amazon.com/images/I/71VZ3A-A82L._AC_SL1500_.jpg", "price": "$13.99", "rating": 4.6, "reviews": 15432, "url": "https://www.amazon.com/dp/B0PT1A"},
        {"rank": 4, "asin": "B0PT2B", "title": "Cat Calming Collar 3 Pack — Adjustable Breakaway Lavender Pheromone Collar for Anxiety Relief", "image": "https://m.media-amazon.com/images/I/71-jOD1XWQL._AC_SL1500_.jpg", "price": "$15.99", "rating": 4.3, "reviews": 6789, "url": "https://www.amazon.com/dp/B0PT2B"},
        {"rank": 6, "asin": "B0PT3C", "title": "WOPET Automatic Dog Feeder 4L — Programmable Auto Pet Food Dispenser with Voice Recorder Timer", "image": "https://m.media-amazon.com/images/I/61OYPKXXDSL._AC_SL1500_.jpg", "price": "$55.99", "rating": 4.4, "reviews": 4312, "url": "https://www.amazon.com/dp/B0PT3C"},
        {"rank": 10, "asin": "B0PT4D", "title": "Dog Poop Bags Extra Thick Leak-Proof — 720 Bags on 48 Rolls Lavender Scented Pet Waste Bags", "image": "https://m.media-amazon.com/images/I/71g-0F4JwCL._AC_SL1500_.jpg", "price": "$16.99", "rating": 4.7, "reviews": 231, "url": "https://www.amazon.com/dp/B0PT4D"},
        {"rank": 15, "asin": "B0PT5E", "title": "Interactive Cat Toys for Indoor Cats — Self-Rotating Electric Ball Automatic LED Flicker Ball", "image": "https://m.media-amazon.com/images/I/71nGqF4AOHL._AC_SL1500_.jpg", "price": "$19.99", "rating": 4.2, "reviews": 43, "url": "https://www.amazon.com/dp/B0PT5E"},
    ],
    "fitness": [
        {"rank": 1, "asin": "B0FT1A", "title": "Resistance Bands Set 5 Pack — Heavy Duty Exercise Bands for Men Women Booty Leg Workout", "image": "https://m.media-amazon.com/images/I/81wB28JF+CL._AC_SL1500_.jpg", "price": "$21.99", "rating": 4.6, "reviews": 31245, "url": "https://www.amazon.com/dp/B0FT1A"},
        {"rank": 3, "asin": "B0FT2B", "title": "Yoga Mat Non Slip 6mm Thick — Eco Friendly Exercise Mat with Carrying Strap for Pilates", "image": "https://m.media-amazon.com/images/I/71yfFD3ZRWL._AC_SL1500_.jpg", "price": "$28.99", "rating": 4.5, "reviews": 12098, "url": "https://www.amazon.com/dp/B0FT2B"},
        {"rank": 5, "asin": "B0FT3C", "title": "GRITIN Resistance Bands 150LBS — Non-Slip Fabric Booty Bands Set for Legs Glutes Hip Training", "image": "https://m.media-amazon.com/images/I/71YJb4UF0UL._AC_SL1500_.jpg", "price": "$16.99", "rating": 4.4, "reviews": 5432, "url": "https://www.amazon.com/dp/B0FT3C"},
        {"rank": 8, "asin": "B0FT4D", "title": "Jump Rope Speed Skipping Rope — Adjustable Steel Cable with Ball Bearings for CrossFit Boxing", "image": "https://m.media-amazon.com/images/I/61lMFAqkWeL._AC_SL1500_.jpg", "price": "$12.99", "rating": 4.5, "reviews": 187, "url": "https://www.amazon.com/dp/B0FT4D"},
        {"rank": 12, "asin": "B0FT5E", "title": "Foam Roller for Muscles — High Density Deep Tissue Massage Roller 13 inch for Back Legs", "image": "https://m.media-amazon.com/images/I/71-4mJGg6dL._AC_SL1500_.jpg", "price": "$24.99", "rating": 4.6, "reviews": 62, "url": "https://www.amazon.com/dp/B0FT5E"},
    ],
    "bebe": [
        {"rank": 2, "asin": "B0BB1A", "title": "Silicone Baby Feeding Set 6 Piece — BPA Free Suction Plate Bowl Fork Spoon Bib for Toddlers", "image": "https://m.media-amazon.com/images/I/71jN0hSYoQL._AC_SL1500_.jpg", "price": "$24.99", "rating": 4.7, "reviews": 9871, "url": "https://www.amazon.com/dp/B0BB1A"},
        {"rank": 5, "asin": "B0BB2B", "title": "Baby Sound Machine White Noise — 31 Soothing Sounds Nightlight Portable Sleep Trainer", "image": "https://m.media-amazon.com/images/I/61-5jVPxv2L._AC_SL1500_.jpg", "price": "$39.99", "rating": 4.6, "reviews": 6234, "url": "https://www.amazon.com/dp/B0BB2B"},
        {"rank": 8, "asin": "B0BB3C", "title": "Mushroom Night Light for Kids — Color Changing Silicone Nursery Lamp with Remote for Baby Room", "image": "https://m.media-amazon.com/images/I/61B4kIgAVpL._AC_SL1500_.jpg", "price": "$18.99", "rating": 4.5, "reviews": 3456, "url": "https://www.amazon.com/dp/B0BB3C"},
        {"rank": 13, "asin": "B0BB4D", "title": "Baby Nail File Electric Trimmer — 6-in-1 Safe Nail Grinder Kit for Newborn Toddler Infant", "image": "https://m.media-amazon.com/images/I/61w1yqKNVcL._AC_SL1500_.jpg", "price": "$16.99", "rating": 4.4, "reviews": 201, "url": "https://www.amazon.com/dp/B0BB4D"},
        {"rank": 18, "asin": "B0BB5E", "title": "Portable Diaper Changing Pad Waterproof — Foldable Travel Mat with Storage Pockets for Baby", "image": "https://m.media-amazon.com/images/I/71K9QDBTYML._AC_SL1500_.jpg", "price": "$22.99", "rating": 4.5, "reviews": 34, "url": "https://www.amazon.com/dp/B0BB5E"},
    ],
    "tech": [
        {"rank": 1, "asin": "B0TL1A", "title": "Anker 65W USB C Charger — 3-Port Compact GaN Foldable Wall Charger for MacBook iPhone Android", "image": "https://m.media-amazon.com/images/I/41TxqPz9XVL._AC_SL1500_.jpg", "price": "$35.99", "rating": 4.7, "reviews": 28654, "url": "https://www.amazon.com/dp/B0TL1A"},
        {"rank": 3, "asin": "B0TL2B", "title": "MagSafe Compatible Phone Stand Ring Holder — 360° Rotation Adjustable Kickstand Mount for iPhone", "image": "https://m.media-amazon.com/images/I/612AUHXH5HL._AC_SL1500_.jpg", "price": "$14.99", "rating": 4.5, "reviews": 11234, "url": "https://www.amazon.com/dp/B0TL2B"},
        {"rank": 6, "asin": "B0TL3C", "title": "PopSockets Phone Grip with MagSafe — Swappable PopGrip Magnetic Stand for iPhone 15 14 13", "image": "https://m.media-amazon.com/images/I/61U0RFT-xPL._AC_SL1500_.jpg", "price": "$24.99", "rating": 4.4, "reviews": 7832, "url": "https://www.amazon.com/dp/B0TL3C"},
        {"rank": 9, "asin": "B0TL4D", "title": "Magnetic Cable Organizer Clips — 6 Pack Desktop Cord Management for USB HDMI Charger Cables", "image": "https://m.media-amazon.com/images/I/71k9J6NQKGL._AC_SL1500_.jpg", "price": "$11.99", "rating": 4.3, "reviews": 423, "url": "https://www.amazon.com/dp/B0TL4D"},
        {"rank": 14, "asin": "B0TL5E", "title": "Screen Cleaning Kit 3-in-1 — Microfiber Cloth Spray Sticker for MacBook iPad iPhone Monitor", "image": "https://m.media-amazon.com/images/I/71Lv+PJCVDL._AC_SL1500_.jpg", "price": "$9.99", "rating": 4.6, "reviews": 67, "url": "https://www.amazon.com/dp/B0TL5E"},
    ],
}


def main():
    cat_map = {c["id"]: c for c in CATEGORIES}
    all_products = {}

    for cat_id, products in MOCK_DATA.items():
        cat = cat_map[cat_id]
        enriched = []
        for p in products:
            p["monthly_sales_est"] = estimate_monthly_sales(p["rank"])
            p["panama"] = score_panama(p, cat)
            enriched.append(p)
        all_products[cat_id] = enriched

    now = datetime.now()
    html = generate_html(all_products, CATEGORIES, now)

    out = Path(__file__).parent / "reports" / "demo.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"✅ Demo report generated: {out}")
    return str(out)


if __name__ == "__main__":
    main()
