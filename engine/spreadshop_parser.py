"""
FBEP Spreadshop Parser

Parses Spreadshop Google Merchant RSS data and groups variants into logical design products.
"""

import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


GOOGLE_NS = {"g": "http://base.google.com/ns/1.0"}


def clean_text(value: str | None) -> str:
    return (value or "").strip()


def parse_price(value: str | None) -> float | None:
    if not value:
        return None

    match = re.search(r"([0-9]+(?:\.[0-9]+)?)", value)

    if not match:
        return None

    return float(match.group(1))


def load_portfolio_designs(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)

        delimiter = ";" if sample.count(";") > sample.count(",") else ","

        reader = csv.DictReader(f, delimiter=delimiter)
        return [dict(row) for row in reader]


def parse_spreadshop_rss(path: str | Path) -> list[dict[str, Any]]:
    tree = ET.parse(path)
    root = tree.getroot()

    items = root.findall("./channel/item")

    variants = []

    for item in items:
        variants.append({
            "id": clean_text(item.findtext("g:id", namespaces=GOOGLE_NS)),
            "item_group_id": clean_text(item.findtext("g:item_group_id", namespaces=GOOGLE_NS)),
            "title": clean_text(item.findtext("g:title", namespaces=GOOGLE_NS)),
            "description": clean_text(item.findtext("g:description", namespaces=GOOGLE_NS)),
            "link": clean_text(item.findtext("g:link", namespaces=GOOGLE_NS)),
            "image_link": clean_text(item.findtext("g:image_link", namespaces=GOOGLE_NS)),
            "availability": clean_text(item.findtext("g:availability", namespaces=GOOGLE_NS)),
            "price": parse_price(item.findtext("g:price", namespaces=GOOGLE_NS)),
            "google_product_category": clean_text(item.findtext("g:google_product_category", namespaces=GOOGLE_NS)),
            "color": clean_text(item.findtext("g:color", namespaces=GOOGLE_NS)),
            "size": clean_text(item.findtext("g:size", namespaces=GOOGLE_NS)),
            "gender": clean_text(item.findtext("g:gender", namespaces=GOOGLE_NS)),
            "age_group": clean_text(item.findtext("g:age_group", namespaces=GOOGLE_NS)),
            "condition": clean_text(item.findtext("g:condition", namespaces=GOOGLE_NS)),
        })

    return variants


def extract_design_id(group_id: str) -> str:
    if not group_id:
        return ""

    parts = group_id.split("_")

    if len(parts) >= 2:
        return "_".join(parts[:-1])

    return group_id


def group_variants_by_design(variants: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}

    for variant in variants:
        group_id = variant.get("item_group_id") or variant.get("id")
        design_id = extract_design_id(group_id)

        if not design_id:
            continue

        groups.setdefault(design_id, []).append(variant)

    return groups


def build_design_products_from_rss(rss_path: str | Path) -> list[dict[str, Any]]:
    variants = parse_spreadshop_rss(rss_path)
    groups = group_variants_by_design(variants)

    products = []

    for group_id, group_variants in groups.items():
        first = group_variants[0]

        colors = sorted({v.get("color", "") for v in group_variants if v.get("color")})
        sizes = sorted({v.get("size", "") for v in group_variants if v.get("size")})
        genders = sorted({v.get("gender", "") for v in group_variants if v.get("gender")})

        products.append({
            "product_id": group_id,
            "source": "spreadshop",
            "partner": "Spreadshop",
            "title": first.get("title", ""),
            "description": first.get("description", ""),
            "category": first.get("google_product_category", ""),
            "price": first.get("price"),
            "currency": "EUR",
            "product_url": first.get("link", ""),
            "affiliate_url": "",
            "image_url": first.get("image_link", ""),
            "status": "active" if first.get("availability") == "in stock" else "draft",
            "brand": "FreeBasics",
            "tags": ["spreadshop", "print-on-demand"] + colors + sizes + genders,
            "compliance_notes": "Spreadshop owned shop product.",
            "variant_count": len(group_variants),
            "colors": colors,
            "sizes": sizes,
            "genders": genders,
        })

    return products
