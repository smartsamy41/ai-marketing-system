import json

from pathlib import Path
from datetime import datetime, timezone

from engine.content_intelligence.geo_local_market_builder import (
    GeoLocalMarketBuilder
)

from engine.content_intelligence.geo_content_node_builder import (
    GeoContentNodeBuilder
)


class GeoReadyCandidateProcessor:

    def __init__(self):

        self.bridge_file = Path(
            "data_master/geo_layer/geo_local_source_bridge.json"
        )

        self.report_file = Path(
            "data_master/geo_layer/geo_ready_candidate_report.json"
        )

        self.market_builder = GeoLocalMarketBuilder()

        self.node_builder = GeoContentNodeBuilder()


    @staticmethod
    def load_json(path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)


    @staticmethod
    def save_json(
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


    def process_record(
        self,
        record
    ):

        if record.get(
            "status"
        ) != "LOCAL_DATA_READY":

            return {

                "status":
                    "SKIPPED",

                "candidate_id":
                    record.get(
                        "candidate_id"
                    ),

                "reason":
                    "local_data_not_ready"
            }


        validation = (
            record.get(
                "validation",
                {}
            )
            or {}
        )


        if validation.get(
            "local_data_available"
        ) is not True:

            return {

                "status":
                    "BLOCKED",

                "candidate_id":
                    record.get(
                        "candidate_id"
                    ),

                "reason":
                    "local_data_validation_failed"
            }


        location_id = record.get(
            "location_id"
        )

        product_id = record.get(
            "product_id"
        )


        try:

            market_result = (
                self.market_builder.build(
                    location_id,
                    product_id
                )
            )

        except Exception as error:

            return {

                "status":
                    "ERROR",

                "candidate_id":
                    record.get(
                        "candidate_id"
                    ),

                "stage":
                    "local_market_builder",

                "error":
                    str(error)
            }


        try:

            node_result = (
                self.node_builder.build(
                    location_id,
                    product_id
                )
            )

        except Exception as error:

            return {

                "status":
                    "ERROR",

                "candidate_id":
                    record.get(
                        "candidate_id"
                    ),

                "stage":
                    "content_node_builder",

                "error":
                    str(error)
            }


        node_validation = (
            node_result.get(
                "validation",
                {}
            )
            or {}
        )


        ready_for_validation = all([

            node_result.get(
                "status"
            )
            == "READY_FOR_GEO_VALIDATION",

            node_validation.get(
                "real_location"
            )
            is True,

            node_validation.get(
                "source_verified"
            )
            is True,

            node_validation.get(
                "wikidata_verified"
            )
            is True,

            node_validation.get(
                "product_match"
            )
            is True,

            node_validation.get(
                "category_match"
            )
            is True,

            node_validation.get(
                "search_intent_match"
            )
            is True,

            node_validation.get(
                "partner_compliant"
            )
            is True,

            node_validation.get(
                "local_data_available"
            )
            is True,

            node_validation.get(
                "unique_content"
            )
            is True

        ])


        return {

            "status":
                (
                    "READY_FOR_GEO_VALIDATION"
                    if ready_for_validation
                    else "BLOCKED"
                ),

            "candidate_id":
                record.get(
                    "candidate_id"
                ),

            "location_id":
                location_id,

            "location_name":
                record.get(
                    "location_name"
                ),

            "product_id":
                product_id,

            "partner":
                record.get(
                    "partner"
                ),

            "market_status":
                "BUILT",

            "node_status":
                node_result.get(
                    "status"
                ),

            "canonical_url":
                node_result.get(
                    "canonical_url"
                ),

            "validation":
                node_validation

        }


    def build(self):

        bridge = self.load_json(
            self.bridge_file
        )


        records = (
            bridge.get(
                "records",
                []
            )
            or []
        )


        ready_records = [
            x
            for x in records
            if x.get(
                "status"
            )
            == "LOCAL_DATA_READY"
        ]


        results = []


        for record in ready_records:

            results.append(
                self.process_record(
                    record
                )
            )


        ready = [
            x
            for x in results
            if x.get(
                "status"
            )
            == "READY_FOR_GEO_VALIDATION"
        ]


        blocked = [
            x
            for x in results
            if x.get(
                "status"
            )
            == "BLOCKED"
        ]


        errors = [
            x
            for x in results
            if x.get(
                "status"
            )
            == "ERROR"
        ]


        output = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "geo_ready_candidate_report",

            "version":
                "1.0",

            "status":
                "ACTIVE",

            "rules":
                {

                    "local_data_ready_required":
                        True,

                    "market_builder_required":
                        True,

                    "content_node_required":
                        True,

                    "unique_content_required":
                        True,

                    "processor_does_not_publish":
                        True

                },

            "summary":
                {

                    "bridge_records":
                        len(
                            records
                        ),

                    "local_data_ready_input":
                        len(
                            ready_records
                        ),

                    "ready_for_geo_validation":
                        len(
                            ready
                        ),

                    "blocked":
                        len(
                            blocked
                        ),

                    "errors":
                        len(
                            errors
                        ),

                    "published":
                        0

                },

            "results":
                results,

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }


        self.save_json(
            self.report_file,
            output
        )


        print(
            "GEO READY CANDIDATE PROCESSOR COMPLETE"
        )

        print(
            "BRIDGE RECORDS:",
            len(
                records
            )
        )

        print(
            "LOCAL DATA READY INPUT:",
            len(
                ready_records
            )
        )

        print(
            "READY FOR GEO VALIDATION:",
            len(
                ready
            )
        )

        print(
            "BLOCKED:",
            len(
                blocked
            )
        )

        print(
            "ERRORS:",
            len(
                errors
            )
        )

        print(
            "PUBLISHED: 0"
        )


        for item in ready:

            print(
                "READY:",
                item.get(
                    "location_name"
                ),
                "|",
                item.get(
                    "product_id"
                ),
                "|",
                item.get(
                    "canonical_url"
                )
            )


        return output


if __name__ == "__main__":

    GeoReadyCandidateProcessor().build()
