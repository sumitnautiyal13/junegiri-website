#!/usr/bin/env python3
"""Add JSON-LD to the pages that had none.

Half the commercial pages shipped with zero structured data -- no schema on
/stay, /retreat, /corporate, /ttc, /adventure or /plan, which is where the
rich-result and AI-citation upside actually is. Every value below is copied
from what the page already says on screen; nothing is invented.

Idempotent -- wrapped in a marker so re-running replaces rather than stacks.
Run via ./build.sh.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://junegirifarms.com"
MARKER = "seo-schema"

ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": "House No-85, Post-Maral, Yamkeshwar",
    "addressLocality": "Pauri Garhwal",
    "addressRegion": "Uttarakhand",
    "postalCode": "249304",
    "addressCountry": "IN",
}
BUSINESS = {"@id": f"{BASE}/#business", "name": "JuneGiri Farms"}

# Verbatim from the "Common questions" section of /retreat.
RETREAT_FAQ = [
    ("I'm a complete beginner. Is this for me?",
     "Yes. Our sessions are alignment-first and beginner-friendly, especially "
     "the gentler Hatha and Yin practices. What matters is that you want to "
     "start, not where you are starting from."),
    ("When do you run the next batch?",
     "We run small-group batches almost every month, Feb-Dec. WhatsApp us and "
     "we'll share the closest upcoming batches and live availability, spots go "
     "fast."),
    ("How do I actually book? Is there a deposit?",
     "WhatsApp us first, we'll share dates, answer questions, and lock your "
     "spot with a 30% deposit. Balance is paid on arrival. It's a "
     "conversation, not a checkout page."),
    ("What's the cancellation policy?",
     "Full refund up to 21 days before arrival. 50% refund between 21 and 7 "
     "days. Non-refundable within 7 days, but you can transfer the booking to "
     "a future batch or a friend."),
    ("Is the food negotiable? I have a dietary restriction.",
     "Fully sattvic (vegetarian, no onion/garlic on request). Gluten-free, "
     "vegan, and allergen-friendly meals are no problem, just tell us when you "
     "book."),
    ("How do I get there?",
     "Nearest station: Haridwar (45 km, 1 hr). Nearest airport: Dehradun Jolly "
     "Grant (35 km). We arrange pickup from both, included in your package."),
    ("Can I come solo? Is it awkward?",
     "Most of our guests come solo. Shared meals, morning practice, and small "
     "group sizes make it easier to connect than any retreat you've been to."),
    ("Can I bring a partner or friend?",
     "Yes, message us on WhatsApp and we'll arrange adjacent rooms or a shared "
     "cottage. Couples and friend duos welcome."),
]

ROOMS = [
    ("Jungle View Room", "/room-jungle", 2500,
     "Forest-facing room with private balcony, queen bed, en-suite. Sleeps 2."),
    ("Neelkanth Stream View Stay", "/room-river", 3500,
     "Standalone stream-view stay with king bed, en-suite, private sit-out."),
    ("Farm Stay Suite", "/room-farm", 4000,
     "Two-bedroom suite with farm view and traditional Pahadi interiors. "
     "Sleeps 4."),
]

# name, price, duration, where -- all lifted from the /adventure cards.
ACTIVITIES = [
    ("River Rafting (16 km)", 1200, "3-4 hours",
     "Shivpuri to Rishikesh. Grade 3+ rapids, certified guides, all gear."),
    ("Bungee Jumping (83m)", 3500, "1 hour",
     "India's highest fixed-platform bungee at Mohan Chatti, operated by "
     "Jumpin Heights."),
    ("Giant Swing (83m)", 3000, "45 min",
     "Step off the cliff, fall 30m before the rope catches, swing across the "
     "gorge."),
    ("Cliff Jumping + Body Surfing", 2200, "Half day",
     "Jump from 30-foot cliffs into Ganga rapids at Neer Garh. Lifejackets and "
     "instructors provided."),
    ("Waterfall Trek", 800, "3 hours",
     "Easy guided trek to Neer Garh or Patna waterfalls. Picnic lunch "
     "included."),
    ("Rajaji Jeep Safari", 4500, "Half day",
     "Wildlife safari into Rajaji National Park. Forest dept. permits "
     "arranged."),
]


def offer(price, unit=None, extra=None):
    data = {"@type": "Offer", "price": str(price), "priceCurrency": "INR"}
    if unit:
        data["priceSpecification"] = {
            "@type": "UnitPriceSpecification",
            "price": str(price),
            "priceCurrency": "INR",
            "unitText": unit,
        }
    if extra:
        data.update(extra)
    return data


def schemas():
    """page stem -> list of JSON-LD objects."""
    return {
        "retreat": [{
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in RETREAT_FAQ
            ],
        }],
        "stay": [{
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Rooms & cottages at JuneGiri Farms",
            "url": f"{BASE}/stay",
            "about": BUSINESS,
            "mainEntity": {
                "@type": "ItemList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i,
                        "item": {
                            "@type": "HotelRoom",
                            "name": f"{name} at JuneGiri Farms",
                            "url": BASE + path,
                            "description": desc,
                            "address": ADDRESS,
                            "telephone": "+91-98738-97652",
                            "offers": offer(price, "per night"),
                        },
                    }
                    for i, (name, path, price, desc) in enumerate(ROOMS, 1)
                ],
            },
        }],
        "corporate": [{
            "@context": "https://schema.org",
            "@type": "Service",
            "name": "Corporate retreats & team offsites at JuneGiri Farms",
            "serviceType": "Corporate retreat",
            "url": f"{BASE}/corporate",
            "provider": {
                "@type": "LodgingBusiness", **BUSINESS,
                "address": ADDRESS, "telephone": "+91-98738-97652",
            },
            "areaServed": {"@type": "Place", "name": "Rishikesh, Uttarakhand"},
            "description": "Custom corporate retreats and team offsites for "
                           "12-40 people at JuneGiri Farms, Rishikesh. "
                           "Full-buyout option available.",
            "offers": offer(5000, "per person per day"),
        }],
        "ttc": [{
            "@context": "https://schema.org",
            "@type": "Course",
            "name": "200-Hour Yoga Teacher Training at JuneGiri Farms",
            "url": f"{BASE}/ttc",
            "description": "200-hour Yoga Alliance certified Teacher Training "
                           "Course at JuneGiri Farms, Rishikesh. Small batches "
                           "of 14, starting Winter 2026.",
            "provider": {
                "@type": "Organization", **BUSINESS, "url": BASE,
            },
            "educationalCredentialAwarded": "200-hour Yoga Alliance certification",
            "inLanguage": "en",
        }],
        "adventure": [{
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Rishikesh adventure activities booked through JuneGiri Farms",
            "url": f"{BASE}/adventure",
            "about": BUSINESS,
            "mainEntity": {
                "@type": "ItemList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": i,
                        "item": {
                            "@type": "Product",
                            "name": name,
                            "description": f"{desc} Duration: {duration}.",
                            "brand": {"@type": "Brand", "name": "JuneGiri Farms"},
                            "offers": offer(price, "per person"),
                        },
                    }
                    for i, (name, price, duration, desc)
                    in enumerate(ACTIVITIES, 1)
                ],
            },
        }],
        "plan": [{
            "@context": "https://schema.org",
            "@type": "BedAndBreakfast",
            **BUSINESS,
            "url": f"{BASE}/plan",
            "image": f"{BASE}/images/surroundings/og-hero.jpg",
            "telephone": "+91-98738-97652",
            "email": "junegirifarms@gmail.com",
            "priceRange": "₹₹",
            "address": ADDRESS,
            "makesOffer": offer(2500, "per person per day", {
                "description": "All-inclusive stay: room, three vegetarian "
                               "meals and tea.",
            }),
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "5.0",
                "reviewCount": "65",
            },
        }],
    }


def apply(stem: str, blocks: list) -> bool:
    page = ROOT / f"{stem}.html"
    html = page.read_text(encoding="utf-8")

    payload = "\n".join(
        '<script type="application/ld+json">'
        + json.dumps(b, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
        for b in blocks
    )
    block = (
        f"<!-- BEGIN {MARKER} — generated by build.sh, edit tools/add-schema.py -->\n"
        f"{payload}\n"
        f"<!-- END {MARKER} -->"
    )

    existing = re.compile(
        rf"<!-- BEGIN {MARKER}.*?<!-- END {MARKER} -->\n?", re.DOTALL
    )
    if existing.search(html):
        updated = existing.sub(block + "\n", html)
    else:
        updated = html.replace("</head>", block + "\n</head>", 1)

    if updated == html:
        return False
    page.write_text(updated, encoding="utf-8")
    return True


def main():
    changed = [stem for stem, blocks in schemas().items() if apply(stem, blocks)]
    print(f"schema: {len(schemas())} pages, {len(changed)} updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
