"""
FBEP Product Catalog Statistics
"""


def catalog_statistics(products):
    by_source = {}
    by_partner = {}
    by_category = {}
    variants_total = 0

    for product in products:
        by_source[product.source] = by_source.get(product.source, 0) + 1
        by_partner[product.partner] = by_partner.get(product.partner, 0) + 1
        by_category[product.category] = by_category.get(product.category, 0) + 1
        variants_total += len(product.variants)

    return {
        "products_total": len(products),
        "variants_total": variants_total,
        "by_source": by_source,
        "by_partner": by_partner,
        "by_category": by_category,
    }
