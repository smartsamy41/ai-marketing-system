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


    def load_json(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:
            return json.load(f)


    def save_json(self, path, data):

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


    @staticmethod
    def clean(value):

        if value is None:
            return ""

        value = str(value).strip()

        if value.lower() in {
            "",
            "nan",
            "none",
            "null"
        }:
            return ""

        return value


    def normalize_location(
        self,
        location
    ):

        location_id = self.clean(
            location.get("location_id")
        )

        name = self.clean(
            location.get("name")
        )

        postal_code = self.clean(
            location.get("postal_code")
        )

        state = self.clean(
            location.get("state")
        )

        country = (
            self.clean(
                location.get("country")
            )
            or "Deutschland"
        )

        source = self.clean(
            location.get("source")
        )

        wikidata_id = self.clean(
            location.get("wikidata_id")
        )

        mediawiki_title = self.clean(
            location.get("mediawiki_title")
        )


        required_ok = all([
            location_id,
            name,
            state,
            country,
            source,
            wikidata_id
        ])


        same_as = []

        if wikidata_id:
            same_as.append(
                f"https://www.wikidata.org/wiki/{wikidata_id}"
            )


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

            "entity": {

                "wikidata_id":
                    wikidata_id,

                "mediawiki_title":
                    mediawiki_title,

                "sameAs":
                    same_as

            },

            "content": {

                "related_products":
                    location.get(
                        "related_products",
                        []
                    )
                    or [],

                "related_categories":
                    location.get(
                        "related_categories",
                        []
                    )
                    or [],

                "articles":
                    location.get(
                        "articles",
                        []
                    )
                    or [],

                "landingpages":
                    location.get(
                        "landingpages",
                        []
                    )
                    or [],

                "faq":
                    location.get(
                        "faq",
                        []
                    )
                    or []

            },

            "sources":
                location.get(
                    "sources",
                    []
                )
                or (
                    [source]
                    if source
                    else []
                ),

            "validation": {

                "real_location":
                    bool(
                        location.get(
                            "real_location",
                            required_ok
                        )
                    ),

                "source_verified":
                    bool(
                        location.get(
                            "source_verified",
                            bool(source)
                        )
                    ),

                "wikidata_verified":
                    bool(
                        location.get(
                            "wikidata_verified",
                            bool(wikidata_id)
                        )
                    ),

                "geo_page_allowed":
                    bool(
                        location.get(
                            "geo_page_allowed",
                            False
                        )
                    )

            },

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }


    def build_registry(
        self,
        locations
    ):

        normalized = []

        seen = set()


        for location in locations:

            item = self.normalize_location(
                location
            )

            location_id = item.get(
                "location_id"
            )


            if not location_id:
                continue


            if location_id in seen:
                continue


            seen.add(
                location_id
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
                "2.0",

            "status":
                "ACTIVE",

            "rules": {

                "real_locations_only":
                    True,

                "source_required":
                    True,

                "wikidata_validation_required":
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
            "GEO LOCATION KNOWLEDGE REGISTRY CREATED"
        )

        print(
            "LOCATIONS:",
            len(
                normalized
            )
        )


        return registry


if __name__ == "__main__":

    builder = GeoLocationKnowledgeBuilder()

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
