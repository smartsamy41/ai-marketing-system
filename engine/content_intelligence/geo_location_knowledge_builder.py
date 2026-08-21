import json

from pathlib import Path
from datetime import datetime, timezone


class GeoLocationKnowledgeBuilder:

    def __init__(self):

        self.location_schema_file = Path(
            "data_master/geo_layer/location_schema.json"
        )

        self.geo_registry_file = Path(
            "data_master/geo_layer/geo_registry.json"
        )


    # =========================================================
    # JSON
    # =========================================================

    def load_json(
        self,
        path
    ):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)


    def save_json(
        self,
        path,
        data
    ):

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )


    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def clean(
        value
    ):

        if value is None:
            return ""

        value = str(
            value
        ).strip()

        if value.lower() in {
            "",
            "nan",
            "none",
            "null"
        }:
            return ""

        return value


    @staticmethod
    def unique_list(
        values
    ):

        output = []
        seen = set()

        for value in values or []:

            if isinstance(
                value,
                dict
            ):

                marker = json.dumps(
                    value,
                    sort_keys=True,
                    ensure_ascii=False
                )

            else:

                marker = str(
                    value
                )

            if marker in seen:
                continue

            seen.add(
                marker
            )

            output.append(
                value
            )

        return output


    # =========================================================
    # ENTITY HELPERS
    # =========================================================

    def get_entity(
        self,
        location
    ):

        entity = (
            location.get(
                "entity",
                {}
            )
            or {}
        )

        if not isinstance(
            entity,
            dict
        ):

            entity = {}

        return entity


    def get_validation(
        self,
        location
    ):

        validation = (
            location.get(
                "validation",
                {}
            )
            or {}
        )

        if not isinstance(
            validation,
            dict
        ):

            validation = {}

        return validation


    # =========================================================
    # NORMALIZE LOCATION
    # =========================================================

    def normalize_location(
        self,
        location
    ):

        entity = self.get_entity(
            location
        )

        old_validation = self.get_validation(
            location
        )


        # -----------------------------------------------------
        # CORE IDENTITY
        # -----------------------------------------------------

        location_id = self.clean(
            location.get(
                "location_id"
            )
        )

        name = self.clean(
            location.get(
                "name"
            )
        )

        postal_code = self.clean(
            location.get(
                "postal_code"
            )
        )

        state = self.clean(
            location.get(
                "state"
            )
        )

        country = (
            self.clean(
                location.get(
                    "country"
                )
            )
            or "Deutschland"
        )


        # -----------------------------------------------------
        # SOURCE
        # -----------------------------------------------------

        source = self.clean(
            location.get(
                "source"
            )
        )

        sources = (
            location.get(
                "sources",
                []
            )
            or []
        )

        if not isinstance(
            sources,
            list
        ):

            sources = [
                sources
            ]

        if not source:

            for item in sources:

                if isinstance(
                    item,
                    dict
                ):

                    source = self.clean(
                        item.get(
                            "source"
                        )
                        or item.get(
                            "name"
                        )
                    )

                    if source:
                        break

                elif item:

                    source = self.clean(
                        item
                    )

                    if source:
                        break


        # -----------------------------------------------------
        # WIKIDATA
        #
        # Unterstützt:
        # location.wikidata_id
        # entity.wikidata_id
        # -----------------------------------------------------

        wikidata_id = self.clean(
            location.get(
                "wikidata_id"
            )
            or entity.get(
                "wikidata_id"
            )
        )

        state_wikidata_id = self.clean(
            location.get(
                "state_wikidata_id"
            )
            or entity.get(
                "state_wikidata_id"
            )
        )

        coordinate = self.clean(
            location.get(
                "coordinate"
            )
            or entity.get(
                "coordinate"
            )
        )

        knowledge_graph = self.clean(
            location.get(
                "knowledge_graph"
            )
            or entity.get(
                "knowledge_graph"
            )
        )

        mediawiki_title = self.clean(
            location.get(
                "mediawiki_title"
            )
            or entity.get(
                "mediawiki_title"
            )
        )


        # -----------------------------------------------------
        # SAME AS
        # -----------------------------------------------------

        same_as = []

        existing_same_as = (
            entity.get(
                "sameAs",
                []
            )
            or []
        )

        if not isinstance(
            existing_same_as,
            list
        ):

            existing_same_as = [
                existing_same_as
            ]

        same_as.extend(
            existing_same_as
        )

        if wikidata_id:

            wikidata_url = (
                "https://www.wikidata.org/wiki/"
                + wikidata_id
            )

            if wikidata_url not in same_as:

                same_as.append(
                    wikidata_url
                )


        # -----------------------------------------------------
        # REQUIRED IDENTITY
        # -----------------------------------------------------

        required_ok = all([
            location_id,
            name,
            state,
            country,
            source,
            wikidata_id
        ])


        # -----------------------------------------------------
        # CONTENT
        # -----------------------------------------------------

        old_content = (
            location.get(
                "content",
                {}
            )
            or {}
        )

        if not isinstance(
            old_content,
            dict
        ):

            old_content = {}

        content = {

            "related_products":
                (
                    location.get(
                        "related_products"
                    )
                    or old_content.get(
                        "related_products"
                    )
                    or []
                ),

            "related_categories":
                (
                    location.get(
                        "related_categories"
                    )
                    or old_content.get(
                        "related_categories"
                    )
                    or []
                ),

            "articles":
                (
                    location.get(
                        "articles"
                    )
                    or old_content.get(
                        "articles"
                    )
                    or []
                ),

            "landingpages":
                (
                    location.get(
                        "landingpages"
                    )
                    or old_content.get(
                        "landingpages"
                    )
                    or []
                ),

            "faq":
                (
                    location.get(
                        "faq"
                    )
                    or old_content.get(
                        "faq"
                    )
                    or []
                )

        }


        # -----------------------------------------------------
        # VALIDATION
        #
        # Bestehende Quality-Werte niemals unbeabsichtigt
        # verlieren.
        # -----------------------------------------------------

        real_location = bool(
            location.get(
                "real_location",
                old_validation.get(
                    "real_location",
                    required_ok
                )
            )
        )

        source_verified = bool(
            location.get(
                "source_verified",
                old_validation.get(
                    "source_verified",
                    bool(source)
                )
            )
        )

        wikidata_verified = bool(
            location.get(
                "wikidata_verified",
                old_validation.get(
                    "wikidata_verified",
                    bool(wikidata_id)
                )
            )
        )

        local_data_available = bool(
            location.get(
                "local_data_available",
                old_validation.get(
                    "local_data_available",
                    False
                )
            )
        )

        product_match = bool(
            location.get(
                "product_match",
                old_validation.get(
                    "product_match",
                    False
                )
            )
        )

        category_match = bool(
            location.get(
                "category_match",
                old_validation.get(
                    "category_match",
                    False
                )
            )
        )

        search_intent_match = bool(
            location.get(
                "search_intent_match",
                old_validation.get(
                    "search_intent_match",
                    False
                )
            )
        )

        partner_compliant = bool(
            location.get(
                "partner_compliant",
                old_validation.get(
                    "partner_compliant",
                    False
                )
            )
        )

        unique_content = bool(
            location.get(
                "unique_content",
                old_validation.get(
                    "unique_content",
                    False
                )
            )
        )

        geo_page_allowed = bool(
            location.get(
                "geo_page_allowed",
                old_validation.get(
                    "geo_page_allowed",
                    False
                )
            )
        )


        # -----------------------------------------------------
        # NORMALIZED OUTPUT
        # -----------------------------------------------------

        return {

            "location_id":
                location_id,

            "name":
                name,

            "postal_code":
                postal_code,

            "state":
                state,

            "country":
                country,

            "entity":
                {

                    "wikidata_id":
                        wikidata_id,

                    "state_wikidata_id":
                        state_wikidata_id,

                    "knowledge_graph":
                        knowledge_graph,

                    "mediawiki_title":
                        mediawiki_title,

                    "sameAs":
                        self.unique_list(
                            same_as
                        ),

                    "coordinate":
                        coordinate

                },

            "content":
                content,

            "sources":
                self.unique_list(
                    sources
                    or (
                        [
                            {
                                "source":
                                    source,

                                "entity":
                                    wikidata_id,

                                "verified":
                                    source_verified
                            }
                        ]
                        if source
                        else []
                    )
                ),

            "validation":
                {

                    "real_location":
                        real_location,

                    "source_verified":
                        source_verified,

                    "wikidata_verified":
                        wikidata_verified,

                    "local_data_available":
                        local_data_available,

                    "product_match":
                        product_match,

                    "category_match":
                        category_match,

                    "search_intent_match":
                        search_intent_match,

                    "partner_compliant":
                        partner_compliant,

                    "unique_content":
                        unique_content,

                    "geo_page_allowed":
                        geo_page_allowed

                },

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }


    # =========================================================
    # BUILD REGISTRY
    # =========================================================

    def build_registry(
        self,
        locations
    ):

        normalized = []

        seen_location_ids = set()

        seen_wikidata_ids = set()

        duplicate_location_ids = []

        duplicate_wikidata_ids = []

        rejected = []


        for location in locations:

            item = self.normalize_location(
                location
            )

            location_id = self.clean(
                item.get(
                    "location_id"
                )
            )

            wikidata_id = self.clean(
                item.get(
                    "entity",
                    {}
                ).get(
                    "wikidata_id"
                )
            )


            # -------------------------------------------------
            # REQUIRED DATA
            # -------------------------------------------------

            if not location_id:

                rejected.append(
                    {
                        "reason":
                            "missing_location_id",

                        "name":
                            item.get(
                                "name"
                            )
                    }
                )

                continue


            if not wikidata_id:

                rejected.append(
                    {
                        "reason":
                            "missing_wikidata_id",

                        "location_id":
                            location_id,

                        "name":
                            item.get(
                                "name"
                            )
                    }
                )

                continue


            # -------------------------------------------------
            # DUPLICATE LOCATION ID
            # -------------------------------------------------

            if location_id in seen_location_ids:

                duplicate_location_ids.append(
                    location_id
                )

                continue


            # -------------------------------------------------
            # DUPLICATE WIKIDATA ENTITY
            #
            # Ein reales Wikidata-Objekt darf nur einmal
            # als Location Entity im Registry-Master stehen.
            # -------------------------------------------------

            if wikidata_id in seen_wikidata_ids:

                duplicate_wikidata_ids.append(
                    wikidata_id
                )

                continue


            seen_location_ids.add(
                location_id
            )

            seen_wikidata_ids.add(
                wikidata_id
            )

            normalized.append(
                item
            )


        registry = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "geo_registry",

            "version":
                "3.0",

            "status":
                "ACTIVE",

            "rules":
                {

                    "real_locations_only":
                        True,

                    "source_required":
                        True,

                    "wikidata_validation_required":
                        True,

                    "wikidata_entity_unique":
                        True,

                    "location_id_unique":
                        True,

                    "no_fake_city_pages":
                        True,

                    "no_fabricated_local_data":
                        True,

                    "quality_shield_required":
                        True

                },

            "count":
                len(
                    normalized
                ),

            "locations":
                normalized,

            "audit":
                {

                    "input_locations":
                        len(
                            locations
                        ),

                    "accepted_locations":
                        len(
                            normalized
                        ),

                    "duplicate_location_ids":
                        duplicate_location_ids,

                    "duplicate_location_id_count":
                        len(
                            duplicate_location_ids
                        ),

                    "duplicate_wikidata_ids":
                        duplicate_wikidata_ids,

                    "duplicate_wikidata_id_count":
                        len(
                            duplicate_wikidata_ids
                        ),

                    "rejected":
                        rejected,

                    "rejected_count":
                        len(
                            rejected
                        )

                },

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }


        self.save_json(
            self.geo_registry_file,
            registry
        )


        print(
            "GEO LOCATION KNOWLEDGE REGISTRY CREATED V3"
        )

        print(
            "INPUT:",
            len(
                locations
            )
        )

        print(
            "LOCATIONS:",
            len(
                normalized
            )
        )

        print(
            "DUPLICATE LOCATION IDS:",
            len(
                duplicate_location_ids
            )
        )

        print(
            "DUPLICATE WIKIDATA IDS:",
            len(
                duplicate_wikidata_ids
            )
        )

        print(
            "REJECTED:",
            len(
                rejected
            )
        )


        return registry


# =============================================================
# DIRECT TEST
# =============================================================

if __name__ == "__main__":

    builder = (
        GeoLocationKnowledgeBuilder()
    )

    current = builder.load_json(
        builder.geo_registry_file
    )

    locations = current.get(
        "locations",
        []
    )

    builder.build_registry(
        locations
    )
