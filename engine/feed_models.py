"""
FBEP Feed Models

Shared product data structures for the Feed Engine.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


VALID_SOURCES = {
    "spreadshop",
    "amazon",
    "check24",
    "tarifcheck",
    "telekom",
}


@dataclass
class FeedProduct:
    product_id: str
    source: str
    partner: str
    title: str
    description: str = ""
    category: str = ""
    price: float | None = None
    currency: str = "EUR"
    product_url: str = ""
    affiliate_url: str = ""
    image_url: str = ""
    status: str = "draft"
    brand: str = ""
    tags: list[str] = field(default_factory=list)
    commission_type: str = ""
    commission_value: float | None = None
    tracking_id: str = ""
    seo_title: str = ""
    meta_description: str = ""
    compliance_notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "product_id": self.product_id,
            "source": self.source,
            "partner": self.partner,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "currency": self.currency,
            "product_url": self.product_url,
            "affiliate_url": self.affiliate_url,
            "image_url": self.image_url,
            "status": self.status,
            "brand": self.brand,
            "tags": ",".join(self.tags),
            "commission_type": self.commission_type,
            "commission_value": self.commission_value,
            "tracking_id": self.tracking_id,
            "seo_title": self.seo_title,
            "meta_description": self.meta_description,
            "compliance_notes": self.compliance_notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FeedProduct":
        tags = data.get("tags", [])
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(",") if tag.strip()]

        return cls(
            product_id=str(data.get("product_id", "")).strip(),
            source=str(data.get("source", "")).strip().lower(),
            partner=str(data.get("partner", "")).strip(),
            title=str(data.get("title", "")).strip(),
            description=str(data.get("description", "")).strip(),
            category=str(data.get("category", "")).strip(),
            price=_safe_float(data.get("price")),
            currency=str(data.get("currency", "EUR")).strip() or "EUR",
            product_url=str(data.get("product_url", "")).strip(),
            affiliate_url=str(data.get("affiliate_url", "")).strip(),
            image_url=str(data.get("image_url", "")).strip(),
            status=str(data.get("status", "draft")).strip() or "draft",
            brand=str(data.get("brand", "")).strip(),
            tags=tags,
            commission_type=str(data.get("commission_type", "")).strip(),
            commission_value=_safe_float(data.get("commission_value")),
            tracking_id=str(data.get("tracking_id", "")).strip(),
            seo_title=str(data.get("seo_title", "")).strip(),
            meta_description=str(data.get("meta_description", "")).strip(),
            compliance_notes=str(data.get("compliance_notes", "")).strip(),
        )


@dataclass
class FeedValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _safe_float(value: Any) -> float | None:
    if value in (None, ""):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None
