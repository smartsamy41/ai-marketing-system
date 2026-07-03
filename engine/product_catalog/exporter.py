"""
FBEP Product Catalog Exporter
"""


CATALOG_SHEET_HEADERS = [
    "fbep_product_id",
    "title",
    "source",
    "source_product_id",
    "partner",
    "category",
    "status",
    "description",
    "product_url",
    "affiliate_url",
    "image_url",
    "tags",
    "variant_count",
    "compliance_notes",
    "created_at",
    "updated_at",
]


def product_to_sheet_row(product):
    return [
        product.fbep_product_id,
        product.title,
        product.source,
        product.source_product_id,
        product.partner,
        product.category,
        product.status,
        product.description,
        product.product_url,
        product.affiliate_url,
        product.image_url,
        ",".join(product.tags),
        len(product.variants),
        product.compliance_notes,
        product.created_at,
        product.updated_at,
    ]


def products_to_sheet_rows(products):
    return [product_to_sheet_row(product) for product in products]
