import json
from pathlib import Path
from datetime import datetime, timezone


class GeoLlmsManifestBuilder:

    GEO_START = "<!-- FREE_BASICS_GEO_AUTO_START -->"
    GEO_END = "<!-- FREE_BASICS_GEO_AUTO_END -->"

    def __init__(self):

        self.nodes_file = Path(
            "data_master/geo_layer/geo_content_nodes.json"
        )

        self.report_file = Path(
            "data_master/geo_layer/geo_batch_report.json"
        )

        self.llms_file = Path(
            "well_known_geo_manifests/llms.txt"
        )

        self.llms_full_file = Path(
            "well_known_geo_manifests/llms-full.txt"
        )

        self.domain = "https://freebasics.online"


    # =========================================================
    # JSON
    # =========================================================

    @staticmethod
    def load_json(path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:
            return json.load(f)


    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def clean(value):

        if value is None:
            return ""

        return str(value).strip()


    @staticmethod
    def unique(values):

        output = []
        seen = set()

        for value in values:

            value = str(
                value or ""
            ).strip()

            if not value:
                continue

            if value in seen:
                continue

            seen.add(value)
            output.append(value)

        return output


    # =========================================================
    # APPROVED GEO NODES
    # =========================================================

    def approved_nodes(self):

        nodes_data = self.load_json(
            self.nodes_file
        )

        report_data = self.load_json(
            self.report_file
        )

        nodes = (
            nodes_data.get(
                "nodes",
                []
            )
            or []
        )

        results = (
            report_data.get(
                "results",
                []
            )
            or []
        )

        # -----------------------------------------------------
        # BATCH REPORT:
        # bestätigt nur die tatsächliche Publishing-Freigabe
        # -----------------------------------------------------

        published_keys = set()

        for result in results:

            validation = (
                result.get(
                    "validation",
                    {}
                )
                or {}
            )

            published_ok = all([

                result.get(
                    "status"
                )
                == "PUBLISHED",

                validation.get(
                    "status"
                )
                == "COMPLIANT",

                validation.get(
                    "geo_quality_status"
                )
                == "INDEX",

                validation.get(
                    "geo_publish_allowed"
                )
                is True,

                validation.get(
                    "llms_allowed"
                )
                is True

            ])

            if not published_ok:
                continue

            key = (
                self.clean(
                    result.get(
                        "product_id"
                    )
                ),
                self.clean(
                    result.get(
                        "location_id"
                    )
                )
            )

            if all(key):
                published_keys.add(key)


        # -----------------------------------------------------
        # GEO CONTENT NODE:
        # bestätigt die eigentliche Datenqualität
        # -----------------------------------------------------

        approved = []

        for node in nodes:

            key = (
                self.clean(
                    node.get(
                        "product_id"
                    )
                ),
                self.clean(
                    node.get(
                        "location_id"
                    )
                )
            )

            if key not in published_keys:
                continue

            validation = (
                node.get(
                    "validation",
                    {}
                )
                or {}
            )

            quality_ok = all([

                validation.get(
                    "real_location"
                )
                is True,

                validation.get(
                    "source_verified"
                )
                is True,

                validation.get(
                    "wikidata_verified"
                )
                is True,

                validation.get(
                    "product_match"
                )
                is True,

                validation.get(
                    "category_match"
                )
                is True,

                validation.get(
                    "search_intent_match"
                )
                is True,

                validation.get(
                    "local_data_available"
                )
                is True,

                validation.get(
                    "partner_compliant"
                )
                is True,

                validation.get(
                    "unique_content"
                )
                is True

            ])

            if not quality_ok:
                continue

            approved.append(node)

        return approved


    # =========================================================
    # SOURCES
    # =========================================================

    def get_sources(
        self,
        node
    ):

        output = []

        # top-level source_urls
        for url in (
            node.get(
                "source_urls",
                []
            )
            or []
        ):
            output.append(url)

        # top-level sources
        for source in (
            node.get(
                "sources",
                []
            )
            or []
        ):

            if isinstance(
                source,
                str
            ):
                output.append(source)

            elif isinstance(
                source,
                dict
            ):

                url = (
                    source.get("url")
                    or source.get("source_url")
                    or source.get("reference")
                )

                if url:
                    output.append(url)

        # primary_sources
        for source in (
            node.get(
                "primary_sources",
                []
            )
            or []
        ):

            if isinstance(
                source,
                str
            ):
                output.append(source)

            elif isinstance(
                source,
                dict
            ):

                url = (
                    source.get("url")
                    or source.get("source_url")
                    or source.get("reference")
                )

                if url:
                    output.append(url)

        # market_data
        market_data = (
            node.get(
                "market_data",
                {}
            )
            or {}
        )

        for url in (
            market_data.get(
                "source_urls",
                []
            )
            or []
        ):
            output.append(url)

        # local_market
        local_market = (
            node.get(
                "local_market",
                {}
            )
            or {}
        )

        for url in (
            local_market.get(
                "source_urls",
                []
            )
            or []
        ):
            output.append(url)

        return self.unique(output)


    # =========================================================
    # WIKIDATA
    # =========================================================

    def wikidata_id(
        self,
        node
    ):

        entity = (
            node.get(
                "entity",
                {}
            )
            or {}
        )

        location = (
            node.get(
                "location",
                {}
            )
            or {}
        )

        return (
            entity.get("wikidata_id")
            or location.get("wikidata_id")
            or node.get("wikidata_id")
            or ""
        )


    # =========================================================
    # LLMS GEO BLOCK
    # =========================================================

    def build_llms_geo_block(
        self,
        nodes
    ):

        lines = [
            self.GEO_START,
            "",
            "## Verified GEO Content",
            ""
        ]

        for node in nodes:

            location = self.clean(
                node.get(
                    "location_name"
                )
            )

            category = self.clean(
                node.get(
                    "category"
                )
            )

            product_id = self.clean(
                node.get(
                    "product_id"
                )
            )

            canonical = self.clean(
                node.get(
                    "canonical_url"
                )
            )

            partner = self.clean(
                node.get(
                    "partner"
                )
            )

            wikidata = self.clean(
                self.wikidata_id(
                    node
                )
            )

            lines.extend([
                f"### {category.title()} in {location}",
                "",
                f"- Canonical: {canonical}",
                f"- Product: {product_id}",
                f"- Partner: {partner}",
                f"- Location: {location}"
            ])

            if wikidata:

                lines.append(
                    f"- Wikidata: {wikidata}"
                )

            lines.extend([
                "- Validation: verified GEO knowledge node",
                ""
            ])

        lines.extend([
            "## GEO Quality Policy",
            "",
            "GEO content is included only when:",
            "",
            "- the location is verified",
            "- source verification succeeded",
            "- Wikidata verification succeeded",
            "- product and category relevance succeeded",
            "- search intent validation succeeded",
            "- local data is available",
            "- unique content validation succeeded",
            "- partner compliance succeeded",
            "- publication validation allows indexing",
            "",
            "Unverified or incomplete GEO nodes are excluded.",
            "",
            self.GEO_END
        ])

        return "\n".join(lines)


    # =========================================================
    # LLMS FULL GEO BLOCK
    # =========================================================

    def build_llms_full_geo_block(
        self,
        nodes
    ):

        now = datetime.now(
            timezone.utc
        ).isoformat()

        lines = [
            self.GEO_START,
            "",
            "## Verified GEO Knowledge Nodes",
            "",
            f"Generated: {now}",
            ""
        ]

        for node in nodes:

            product_id = self.clean(
                node.get(
                    "product_id"
                )
            )

            category = self.clean(
                node.get(
                    "category"
                )
            )

            silo = self.clean(
                node.get(
                    "silo"
                )
            )

            location = self.clean(
                node.get(
                    "location_name"
                )
            )

            location_id = self.clean(
                node.get(
                    "location_id"
                )
            )

            canonical = self.clean(
                node.get(
                    "canonical_url"
                )
            )

            partner = self.clean(
                node.get(
                    "partner"
                )
            )

            wikidata = self.clean(
                self.wikidata_id(
                    node
                )
            )

            sources = self.get_sources(
                node
            )

            lines.extend([
                f"### {category.title()} in {location}",
                "",
                "Canonical:",
                canonical,
                "",
                "Product:",
                product_id,
                "",
                "Partner:",
                partner,
                "",
                "Category:",
                category,
                "",
                "Silo:",
                silo,
                "",
                "Location:",
                location,
                "",
                "Location ID:",
                location_id,
                ""
            ])

            if wikidata:

                lines.extend([
                    "Wikidata:",
                    wikidata,
                    ""
                ])

            lines.extend([
                "Validation:",
                "- real_location: true",
                "- source_verified: true",
                "- wikidata_verified: true",
                "- product_match: true",
                "- category_match: true",
                "- search_intent_match: true",
                "- local_data_available: true",
                "- partner_compliant: true",
                "- unique_content: true",
                "- geo_quality_status: INDEX",
                "- geo_publish_allowed: true",
                "- llms_allowed: true",
                "",
                "Primary sources:"
            ])

            if sources:

                for source in sources:
                    lines.append(
                        f"- {source}"
                    )

            else:

                lines.append(
                    "- Source references stored in GEO knowledge registry"
                )

            lines.extend([
                "",
                "---",
                ""
            ])

        lines.extend([
            "## Machine Interpretation Policy",
            "",
            "Only validated and published GEO nodes are included.",
            "",
            "A location name alone does not qualify a page for inclusion.",
            "",
            "Missing local data, missing source verification or failed "
            "quality validation prevents inclusion.",
            "",
            self.GEO_END
        ])

        return "\n".join(lines)


    # =========================================================
    # BASE LLMS
    # =========================================================

    def default_llms_base(self):

        return """# Free Basics

Name:
Free Basics

Website:
https://freebasics.online

Description:
Free Basics is a knowledge and content platform for products,
guides, comparisons and selected partner offers.

Knowledge Structure:

- Product Catalog: 44 products
- Product Entities
- Knowledge Graph
- GEO optimized content
- Source based information

Main Areas:

- Technology and Internet
- Energy
- Finance
- Insurance
- Travel
- Everyday Products

Machine Readable Data:

- /datasets/verified-products.json
- /datasets/verified-products.jsonld
- /datasets/knowledge-graph.json

Content Structure:

- Landingpages
- Blog Articles
- Knowledge Articles
- Product Information
- Verified GEO Content

Transparency:

Free Basics clearly discloses affiliate relationships.
Partner content is marked as advertising where applicable.

Sources:

- Primary source documents
- Official partner information
- Public knowledge sources
- Verified local GEO sources

Legal:

- https://freebasics.online/impressum
- https://freebasics.online/datenschutz
- https://freebasics.online/affiliate-hinweis
- https://freebasics.online/kontakt
"""


    # =========================================================
    # BASE LLMS FULL
    # =========================================================

    def default_llms_full_base(self):

        return """# Free Basics - Full Knowledge Manifest

## Identity

Name:
Free Basics

Website:
https://freebasics.online

System:
FREE BASICS AI MARKETING SYSTEM


## Purpose

Free Basics provides structured information,
guides and product knowledge.

The platform combines:

- Product information
- Knowledge articles
- GEO optimized content
- Source based information
- Partner offer references


## Product Knowledge Layer

Current Product Catalog:

44 Products


## Data Architecture

Main Data Sources:

/datasets/verified-products.json

/datasets/verified-products.jsonld

/datasets/knowledge-graph.json


## Knowledge Graph

Entities:

- Products
- Partners
- Categories
- Locations

Relations:

- provided_by
- belongs_to
- related_to
- located_in


## Content System

Content types:

- Landingpages
- Blog Articles
- Knowledge Guides
- Product Information
- Verified GEO Content


## GEO Architecture

Verified GEO content is generated only from:

- validated real locations
- verified source references
- Wikidata entity validation
- verified product/category relationships
- verified search intent
- real local data
- unique content validation
- partner compliance validation


## Canonical Policy

Original content is published first on Free Basics.

External distribution must reference the original source.


## Transparency

Affiliate relationships are disclosed.

Partner content is marked as advertising where applicable.

Free Basics acts as information provider and Tippgeber.


## Data Quality

The system uses:

- Verified product records
- Source references
- Structured datasets
- Automated validation
- GEO Quality Shield


## Legal Information

Imprint:
https://freebasics.online/impressum

Privacy:
https://freebasics.online/datenschutz

Affiliate Information:
https://freebasics.online/affiliate-hinweis


## Machine Access

Available structured resources:

- Product Dataset
- JSON-LD Dataset
- Knowledge Graph
- API Documentation
- llms.txt
- llms-full.txt


Status:

ACTIVE
"""


    # =========================================================
    # AUTO BLOCK REPLACEMENT
    # =========================================================

    def replace_geo_block(
        self,
        existing,
        geo_block,
        default_base
    ):

        existing = str(
            existing or ""
        )

        if not existing.strip():

            existing = (
                default_base.rstrip()
            )

        start = existing.find(
            self.GEO_START
        )

        end = existing.find(
            self.GEO_END
        )

        if (
            start != -1
            and end != -1
            and end >= start
        ):

            end = (
                end
                + len(
                    self.GEO_END
                )
            )

            before = (
                existing[:start]
                .rstrip()
            )

            after = (
                existing[end:]
                .lstrip()
            )

            output = (
                before
                + "\n\n"
                + geo_block
            )

            if after:

                output += (
                    "\n\n"
                    + after
                )

            return (
                output.rstrip()
                + "\n"
            )

        return (
            existing.rstrip()
            + "\n\n"
            + geo_block
            + "\n"
        )


    # =========================================================
    # BUILD
    # =========================================================

    def build(self):

        nodes = self.approved_nodes()

        llms_geo = (
            self.build_llms_geo_block(
                nodes
            )
        )

        llms_full_geo = (
            self.build_llms_full_geo_block(
                nodes
            )
        )

        current_llms = ""

        if self.llms_file.exists():

            current_llms = (
                self.llms_file.read_text(
                    encoding="utf-8"
                )
            )

        # Die V1 hatte die Datei überschrieben.
        # Wenn die Basisstruktur fehlt, wird sie wiederhergestellt.

        if (
            "Knowledge Structure:"
            not in current_llms
        ):

            current_llms = (
                self.default_llms_base()
            )

        current_llms_full = ""

        if self.llms_full_file.exists():

            current_llms_full = (
                self.llms_full_file.read_text(
                    encoding="utf-8"
                )
            )

        if (
            "## Identity"
            not in current_llms_full
        ):

            current_llms_full = (
                self.default_llms_full_base()
            )

        final_llms = self.replace_geo_block(
            current_llms,
            llms_geo,
            self.default_llms_base()
        )

        final_llms_full = self.replace_geo_block(
            current_llms_full,
            llms_full_geo,
            self.default_llms_full_base()
        )

        self.llms_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.llms_file.write_text(
            final_llms,
            encoding="utf-8"
        )

        self.llms_full_file.write_text(
            final_llms_full,
            encoding="utf-8"
        )

        result = {

            "status":
                "UPDATED",

            "geo_nodes":
                len(nodes),

            "llms":
                str(
                    self.llms_file
                ),

            "llms_full":
                str(
                    self.llms_full_file
                )
        }

        print(
            "GEO LLMS MANIFEST UPDATED V3"
        )

        print(
            "GEO NODES:",
            len(nodes)
        )

        print(
            "LLMS:",
            self.llms_file
        )

        print(
            "LLMS FULL:",
            self.llms_full_file
        )

        return result


if __name__ == "__main__":

    GeoLlmsManifestBuilder().build()
