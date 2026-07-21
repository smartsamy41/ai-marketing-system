import json
from typing import Dict, Any, Optional


def generate_product_schema(
    name: str,
    description: str,
    url: str,
    price: str | None = None,
    currency: str = "EUR"
) -> str:

    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "description": description
    }

    if price and str(price).strip() not in {"0", "0.00", "None", "nan"}:
        schema["offers"] = {
            "@type": "Offer",
            "priceCurrency": currency,
            "price": str(price),
            "url": url,
            "availability": "https://schema.org/InStock"
        }

    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'



def generate_article_schema(title: str, description: str, url: str, date_published: str) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        },
        "datePublished": date_published,
        "author": {
            "@type": "Organization",
            "name": "Free Basics Redaktion"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Free Basics"
        }
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'
