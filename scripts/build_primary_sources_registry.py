import json
from datetime import datetime, timezone


OUTPUT = "knowledge/sources/primary_sources.json"


def main():

    sources = [

        {
            "source_id": "SRC_CHECK24",
            "name": "CHECK24 Partnerdaten",
            "type": "partner_source",
            "category": "comparison",
            "usage": "Affiliate product information",
            "status": "active"
        },

        {
            "source_id": "SRC_TARIFCHECK",
            "name": "TARIFCHECK Partnerdaten",
            "type": "partner_source",
            "category": "comparison",
            "usage": "Affiliate product information",
            "status": "active"
        },

        {
            "source_id": "SRC_AMAZON",
            "name": "Amazon PartnerNet",
            "type": "partner_source",
            "category": "commerce",
            "usage": "Product information",
            "status": "active"
        },

        {
            "source_id": "SRC_TELEKOM",
            "name": "Telekom Profis Shop",
            "type": "partner_source",
            "category": "telecommunication",
            "usage": "Direct shop routing",
            "status": "active"
        },

        {
            "source_id": "SRC_SCHEMA_ORG",
            "name": "Schema.org",
            "type": "structured_data_standard",
            "category": "semantic_web",
            "usage": "JSON-LD knowledge graph markup",
            "status": "active"
        },

        {
            "source_id": "SRC_WIKIDATA",
            "name": "Wikidata",
            "type": "knowledge_base",
            "category": "entity_reference",
            "usage": "Entity linking",
            "status": "planned"
        }

    ]


    registry = {

        "version": "1.0",

        "system": "FREE BASICS AI MARKETING SYSTEM",

        "description":
            "Primary Source Registry for GEO Knowledge Graph",

        "generated_at":
            datetime.now(
                timezone.utc
            ).isoformat(),

        "status":
            "ACTIVE",

        "count":
            len(sources),

        "sources":
            sources

    }


    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            registry,
            f,
            indent=2,
            ensure_ascii=False
        )


    print("PRIMARY SOURCE REGISTRY READY")
    print("Sources:", len(sources))


if __name__ == "__main__":
    main()
