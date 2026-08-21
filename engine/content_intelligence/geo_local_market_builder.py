import json
from pathlib import Path
from datetime import datetime, timezone


class GeoLocalMarketBuilder:

    def __init__(self):

        self.sources_file = Path(
            "data_master/geo_and_entities/primary_sources_index.json"
        )

        self.geo_registry_file = Path(
            "data_master/geo_layer/geo_registry.json"
        )

        self.output_file = Path(
            "data_master/geo_layer/local_market_registry.json"
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


    def get_location(
        self,
        location_id
    ):

        registry = self.load_json(
            self.geo_registry_file
        )

        for location in registry.get(
            "locations",
            []
        ):

            if location.get(
                "location_id"
            ) == location_id:

                return location

        return {}


    def get_verified_sources(
        self,
        location_id,
        product_id
    ):

        data = self.load_json(
            self.sources_file
        )

        results = []


        for source in data.get(
            "sources",
            []
        ):

            if (
                source.get("location_id") == location_id
                and
                source.get("product_id") == product_id
                and
                source.get("source_verified") is True
                and
                source.get("status") == "active"
            ):

                results.append(
                    source
                )


        return results


    def build_record(
        self,
        location_id,
        product_id
    ):

        location = self.get_location(
            location_id
        )


        if not location:

            return {
                "status": "BLOCKED",
                "reason": "location_not_found"
            }


        sources = self.get_verified_sources(
            location_id,
            product_id
        )


        verified_facts = []


        for source in sources:

            for fact in source.get(
                "verified_facts",
                []
            ):

                if fact not in verified_facts:

                    verified_facts.append(
                        fact
                    )


        source_ids = [

            source.get(
                "source_id"
            )

            for source in sources

            if source.get(
                "source_id"
            )

        ]


        source_urls = [

            source.get(
                "url"
            )

            for source in sources

            if source.get(
                "url"
            )

        ]


        local_data_available = bool(
            sources
            and verified_facts
        )


        record = {

            "location_id":
                location_id,

            "location_name":
                location.get(
                    "name",
                    ""
                ),

            "postal_code":
                location.get(
                    "postal_code",
                    ""
                ),

            "state":
                location.get(
                    "state",
                    ""
                ),

            "country":
                location.get(
                    "country",
                    "Deutschland"
                ),

            "product_id":
                product_id,

            "category":
                "strom",

            "silo":
                "energie",

            "market_data": {

                "verified_facts":
                    verified_facts,

                "source_ids":
                    source_ids,

                "source_urls":
                    source_urls,

                "source_count":
                    len(
                        sources
                    )

            },

            "validation": {

                "real_location":
                    bool(
                        location.get(
                            "validation",
                            {}
                        ).get(
                            "real_location"
                        )
                    ),

                "source_verified":
                    all(
                        source.get(
                            "source_verified"
                        )
                        is True
                        for source in sources
                    )
                    if sources
                    else False,

                "local_data_available":
                    local_data_available,

                "unique_content":
                    False,

                "geo_page_allowed":
                    False

            },

            "status":
                (
                    "LOCAL_DATA_READY"
                    if local_data_available
                    else "LOCAL_DATA_MISSING"
                ),

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }


        return record


    def build(
        self,
        location_id,
        product_id
    ):

        record = self.build_record(
            location_id,
            product_id
        )


        existing = self.load_json(
            self.output_file
        )


        records = existing.get(
            "records",
            []
        )


        records = [

            x for x in records

            if not (
                x.get(
                    "location_id"
                ) == location_id
                and
                x.get(
                    "product_id"
                ) == product_id
            )

        ]


        records.append(
            record
        )


        output = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "geo_local_market_registry",

            "version":
                "1.0",

            "status":
                "ACTIVE",

            "rules": {

                "verified_sources_only":
                    True,

                "no_fabricated_local_data":
                    True,

                "source_required":
                    True,

                "unique_content_required_for_index":
                    True

            },

            "count":
                len(
                    records
                ),

            "records":
                records,

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }


        self.save_json(
            self.output_file,
            output
        )


        print(
            "GEO LOCAL MARKET REGISTRY UPDATED"
        )

        print(
            "RECORDS:",
            len(
                records
            )
        )

        print(
            "LOCATION:",
            record.get(
                "location_name"
            )
        )

        print(
            "PRODUCT:",
            record.get(
                "product_id"
            )
        )

        print(
            "SOURCE COUNT:",
            record.get(
                "market_data",
                {}
            ).get(
                "source_count"
            )
        )

        print(
            "LOCAL DATA AVAILABLE:",
            record.get(
                "validation",
                {}
            ).get(
                "local_data_available"
            )
        )

        print(
            "UNIQUE CONTENT:",
            record.get(
                "validation",
                {}
            ).get(
                "unique_content"
            )
        )

        print(
            "GEO PAGE ALLOWED:",
            record.get(
                "validation",
                {}
            ).get(
                "geo_page_allowed"
            )
        )


        return output


if __name__ == "__main__":

    GeoLocalMarketBuilder().build(
        "DE-SH-LUEBECK-Q2843",
        "CHK24_001"
    )
