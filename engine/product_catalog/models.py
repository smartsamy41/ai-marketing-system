"""
FBEP Product Catalog Models
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ProductSource:
    source: str
    source_product_id: str
    partner: str
    url: str = ""


@dataclass
class ProductVariant:
    variant_id: str
    title: str = ""
    product_type: str = ""
    color: str = ""
    size: str = ""
    gender: str = ""
    price: float | None = None
    currency: str = "EUR"
    image_url: str = ""
    product_url: str = ""
    status: str = "active"


@dataclass
class CatalogProduct:
    fbep_product_id: str
    title: str
    source: str
    source_product_id: str
    partner: str
    category: str = ""
    status: str = "draft"
    description: str = ""
    product_url: str = ""
    affiliate_url: str = ""
    image_url: str = ""
    tags: list[str] = field(default_factory=list)
    variants: list[ProductVariant] = field(default_factory=list)
    sources: list[ProductSource] = field(default_factory=list)
    seo: dict[str, Any] = field(default_factory=dict)
    publishing: dict[str, Any] = field(default_factory=dict)
    analytics: dict[str, Any] = field(default_factory=dict)
    learning: dict[str, Any] = field(default_factory=dict)
    compliance_notes: str = ""
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "fbep_product_id": self.fbep_product_id,
            "title": self.title,
            "source": self.source,
            "source_product_id": self.source_product_id,
            "partner": self.partner,
            "category": self.category,
            "status": self.status,
            "description": self.description,
            "product_url": self.product_url,
            "affiliate_url": self.affiliate_url,
            "image_url": self.image_url,
            "tags": self.tags,
            "variants": [v.__dict__ for v in self.variants],
            "sources": [s.__dict__ for s in self.sources],
            "seo": self.seo,
            "publishing": self.publishing,
            "analytics": self.analytics,
            "learning": self.learning,
            "compliance_notes": self.compliance_notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
