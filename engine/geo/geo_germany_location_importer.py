import json
import time

from pathlib import Path
from datetime import datetime, timezone

from adapters.research_and_wiki_adapters.wikidata_sparql_adapter.wikidata_client import (
    WikidataClient
)

from engine.content_intelligence.geo_location_knowledge_builder import (
    GeoLocationKnowledgeBuilder
)


class GeoGermanyLocationImporter:

    def __init__(self):

        self.wikidata = WikidataClient()
        self.registry_builder = GeoLocationKnowledgeBuilder()

        self.registry_file = Path(
            "data_master/geo_layer/geo_registry.json"
        )

        self.report_file = Path(
            "data_master/geo_layer/germany_location_import_report.json"
        )

        self.seed_file = Path(
            "data_master/geo_layer/germany_location_seed.json"
        )

        # =====================================================
        # VERIFIED PILOT
        # Keine Namenssuche.
        # Jede Stadt besitzt eine eindeutige Wikidata-QID.
        # =====================================================

        self.default_seed = [

            {
                "name": "Berlin",
                "wikidata_id": "Q64",
                "state": "Berlin",
                "state_code": "BE",
                "state_wikidata_id": "Q64"
            },

            {
                "name": "Hamburg",
                "wikidata_id": "Q1055",
                "state": "Hamburg",
                "state_code": "HH",
                "state_wikidata_id": "Q1055"
            },

            {
                "name": "München",
                "wikidata_id": "Q1726",
                "state": "Bayern",
                "state_code": "BY",
                "state_wikidata_id": "Q980"
            },

            {
                "name": "Köln",
                "wikidata_id": "Q365",
                "state": "Nordrhein-Westfalen",
                "state_code": "NW",
                "state_wikidata_id": "Q1198"
            },

            {
                "name": "Frankfurt am Main",
                "wikidata_id": "Q1794",
                "state": "Hessen",
                "state_code": "HE",
                "state_wikidata_id": "Q1199"
            },

            {
                "name": "Stuttgart",
                "wikidata_id": "Q1022",
                "state": "Baden-Württemberg",
                "state_code": "BW",
                "state_wikidata_id": "Q985"
            },

            {
                "name": "Düsseldorf",
                "wikidata_id": "Q1718",
                "state": "Nordrhein-Westfalen",
                "state_code": "NW",
                "state_wikidata_id": "Q1198"
            },

            {
                "name": "Leipzig",
                "wikidata_id": "Q2079",
                "state": "Sachsen",
                "state_code": "SN",
                "state_wikidata_id": "Q1202"
            },

            {
                "name": "Dortmund",
                "wikidata_id": "Q1295",
                "state": "Nordrhein-Westfalen",
                "state_code": "NW",
                "state_wikidata_id": "Q1198"
            },

            {
                "name": "Lübeck",
                "wikidata_id": "Q2843",
                "state": "Schleswig-Holstein",
                "state_code": "SH",
                "state_wikidata_id": "Q1194"
            }

        ]


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


    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def clean(value):

        if value is None:
            return ""

        return str(
            value
        ).strip()


    @staticmethod
    def slug(value):

        return (
            str(value or "")
            .strip()
            .upper()
            .replace("Ä", "AE")
            .replace("Ö", "OE")
            .replace("Ü", "UE")
            .replace("ß", "SS")
            .replace(" ", "-")
            .replace("/", "-")
        )


    # =========================================================
    # SEED
    # =========================================================

    def ensure_seed(self):

        data = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "germany_location_seed",

            "version":
                "2.0",

            "status":
                "VERIFIED_PILOT",

            "rules":
                {

                    "qid_required":
                        True,

                    "no_name_guessing":
                        True,

                    "real_locations_only":
                        True,

                    "no_auto_geo_publish":
                        True

                },

            "locations":
                self.default_seed,

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()

        }

        self.save_json(
            self.seed_file,
            data
        )

        return data


    # =========================================================
    # EXACT QID QUERY
    # =========================================================

    def query_qid(
        self,
        wikidata_id
    ):

        qid = self.clean(
            wikidata_id
        )

        if not qid.startswith("Q"):

            raise ValueError(
                f"Invalid Wikidata ID: {qid}"
            )

        query = f"""
        SELECT DISTINCT
            ?item
            ?itemLabel
            ?postalCode
            ?coordinate
        WHERE {{

            BIND(
                wd:{qid}
                AS ?item
            )

            OPTIONAL {{
                ?item wdt:P281 ?postalCode.
            }}

            OPTIONAL {{
                ?item wdt:P625 ?coordinate.
            }}

            SERVICE wikibase:label {{
                bd:serviceParam wikibase:language "de".
            }}

        }}

        LIMIT 20
        """

        return self.wikidata.query(
            query
        )


    # =========================================================
    # PARSE EXACT ENTITY
    # =========================================================

    def parse_qid_result(
        self,
        seed,
        raw
    ):

        bindings = (
            raw
            .get(
                "results",
                {}
            )
            .get(
                "bindings",
                []
            )
        )

        if not bindings:

            return None

        postal_codes = []

        coordinate = ""

        label = self.clean(
            seed.get(
                "name"
            )
        )

        for row in bindings:

            item_label = (
                row
                .get(
                    "itemLabel",
                    {}
                )
                .get(
                    "value",
                    ""
                )
            )

            if item_label:
                label = item_label

            postal = (
                row
                .get(
                    "postalCode",
                    {}
                )
                .get(
                    "value",
                    ""
                )
            )

            if postal:

                if postal not in postal_codes:
                    postal_codes.append(
                        postal
                    )

            coord = (
                row
                .get(
                    "coordinate",
                    {}
                )
                .get(
                    "value",
                    ""
                )
            )

            if (
                coord
                and not coordinate
            ):

                coordinate = coord


        postal_code = ""

        if postal_codes:

            postal_code = " | ".join(
                postal_codes
            )


        return {

            "label":
                label,

            "postal_code":
                postal_code,

            "coordinate":
                coordinate

        }


    # =========================================================
    # CREATE LOCATION
    # =========================================================

    def build_location(
        self,
        seed,
        wikidata_data
    ):

        name = self.clean(
            seed.get(
                "name"
            )
        )

        qid = self.clean(
            seed.get(
                "wikidata_id"
            )
        )

        state = self.clean(
            seed.get(
                "state"
            )
        )

        state_code = self.clean(
            seed.get(
                "state_code"
            )
        )

        state_qid = self.clean(
            seed.get(
                "state_wikidata_id"
            )
        )


        location_id = (
            "DE-"
            + state_code
            + "-"
            + self.slug(
                name
            )
            + "-"
            + qid
        )


        return {

            "location_id":
                location_id,

            "name":
                name,

            "postal_code":
                self.clean(
                    wikidata_data.get(
                        "postal_code"
                    )
                ),

            "state":
                state,

            "country":
                "Deutschland",

            "source":
                "Wikidata SPARQL",

            "wikidata_id":
                qid,

            "state_wikidata_id":
                state_qid,

            "coordinate":
                self.clean(
                    wikidata_data.get(
                        "coordinate"
                    )
                ),

            "mediawiki_title":
                name,

            "real_location":
                True,

            "source_verified":
                True,

            "wikidata_verified":
                True,

            # -------------------------------------------------
            # Import bedeutet noch KEINE Veröffentlichung.
            # -------------------------------------------------

            "local_data_available":
                False,

            "product_match":
                False,

            "category_match":
                False,

            "search_intent_match":
                False,

            "partner_compliant":
                False,

            "unique_content":
                False,

            "geo_page_allowed":
                False,

            "sources":
                [
                    {
                        "source":
                            "Wikidata SPARQL",

                        "entity":
                            qid,

                        "url":
                            (
                                "https://www.wikidata.org/wiki/"
                                + qid
                            ),

                        "verified":
                            True
                    }
                ]

        }


    # =========================================================
    # IMPORT ONE
    # =========================================================

    def import_one(
        self,
        seed
    ):

        name = self.clean(
            seed.get(
                "name"
            )
        )

        qid = self.clean(
            seed.get(
                "wikidata_id"
            )
        )

        try:

            raw = self.query_qid(
                qid
            )

        except Exception as error:

            return {

                "status":
                    "ERROR",

                "name":
                    name,

                "wikidata_id":
                    qid,

                "error":
                    str(error)

            }


        parsed = self.parse_qid_result(
            seed,
            raw
        )


        if not parsed:

            return {

                "status":
                    "NOT_FOUND",

                "name":
                    name,

                "wikidata_id":
                    qid

            }


        location = self.build_location(
            seed,
            parsed
        )


        return {

            "status":
                "READY",

            "location":
                location

        }


    # =========================================================
    # REBUILD VERIFIED PILOT REGISTRY
    # =========================================================

    def run(
        self,
        limit=None
    ):

        seed_data = self.ensure_seed()

        seeds = (
            seed_data.get(
                "locations",
                []
            )
            or []
        )

        if limit is not None:

            seeds = seeds[
                :int(limit)
            ]


        # -----------------------------------------------------
        # WICHTIG:
        # Pilot wird bewusst vollständig aus verifizierten
        # QIDs neu aufgebaut.
        #
        # Die fehlerhaften Namens-Suchergebnisse werden
        # NICHT übernommen.
        # -----------------------------------------------------

        locations = []

        results = []

        imported = 0
        failed = 0


        for seed in seeds:

            result = self.import_one(
                seed
            )

            if result.get(
                "status"
            ) != "READY":

                failed += 1

                results.append(
                    result
                )

                continue


            location = result[
                "location"
            ]

            locations.append(
                location
            )

            imported += 1


            results.append(
                {

                    "status":
                        "IMPORTED",

                    "location_id":
                        location.get(
                            "location_id"
                        ),

                    "name":
                        location.get(
                            "name"
                        ),

                    "state":
                        location.get(
                            "state"
                        ),

                    "wikidata_id":
                        location.get(
                            "wikidata_id"
                        ),

                    "postal_code":
                        location.get(
                            "postal_code"
                        )

                }
            )


            time.sleep(
                0.25
            )


        registry = (
            self.registry_builder
            .build_registry(
                locations
            )
        )


        report = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "germany_location_import_report",

            "version":
                "2.0",

            "created":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "summary":
                {

                    "seed_locations":
                        len(
                            seeds
                        ),

                    "imported":
                        imported,

                    "failed":
                        failed,

                    "registry_after":
                        registry.get(
                            "count",
                            0
                        ),

                    "duplicate_wikidata_ids":
                        (
                            registry
                            .get(
                                "audit",
                                {}
                            )
                            .get(
                                "duplicate_wikidata_id_count",
                                0
                            )
                        )

                },

            "results":
                results

        }


        self.save_json(
            self.report_file,
            report
        )


        print(
            "GERMANY GEO VERIFIED PILOT IMPORT V2"
        )

        print(
            "SEED:",
            len(
                seeds
            )
        )

        print(
            "IMPORTED:",
            imported
        )

        print(
            "FAILED:",
            failed
        )

        print(
            "REGISTRY:",
            registry.get(
                "count",
                0
            )
        )

        print(
            "DUPLICATE QIDS:",
            (
                registry
                .get(
                    "audit",
                    {}
                )
                .get(
                    "duplicate_wikidata_id_count",
                    0
                )
            )
        )

        print(
            "REPORT:",
            self.report_file
        )


        return report


if __name__ == "__main__":

    GeoGermanyLocationImporter().run()
