import json

from pathlib import Path
from datetime import datetime, timezone


class GeoLocalSourceBridge:

    def __init__(self):

        self.candidate_file = Path(
            "data_master/geo_layer/geo_candidate_matrix.json"
        )

        self.sources_file = Path(
            "data_master/geo_and_entities/primary_sources_index.json"
        )

        self.output_file = Path(
            "data_master/geo_layer/geo_local_source_bridge.json"
        )


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

        return str(value).strip()


    @staticmethod
    def unique(values):

        output = []
        seen = set()

        for value in values or []:

            marker = json.dumps(
                value,
                sort_keys=True,
                ensure_ascii=False
            )

            if marker in seen:
                continue

            seen.add(marker)
            output.append(value)

        return output


    # =========================================================
    # VERIFIED LOCAL SOURCES
    # =========================================================

    def verified_local_sources(
        self,
        location_id,
        product_id
    ):

        data = self.load_json(
            self.sources_file
        )

        results = []

        for source in (
            data.get(
                "sources",
                []
            )
            or []
        ):

            if source.get(
                "type"
            ) != "official_local_source":

                continue


            if self.clean(
                source.get(
                    "location_id"
                )
            ) != self.clean(
                location_id
            ):

                continue


            if self.clean(
                source.get(
                    "product_id"
                )
            ) != self.clean(
                product_id
            ):

                continue


            if source.get(
                "source_verified"
            ) is not True:

                continue


            if source.get(
                "status"
            ) != "active":

                continue


            results.append(
                source
            )


        return results


    # =========================================================
    # FACTS
    # =========================================================

    def collect_facts(
        self,
        sources
    ):

        facts = []

        for source in sources:

            for fact in (
                source.get(
                    "verified_facts",
                    []
                )
                or []
            ):

                fact = self.clean(
                    fact
                )

                if (
                    fact
                    and fact not in facts
                ):

                    facts.append(
                        fact
                    )


        return facts


    # =========================================================
    # SOURCE IDS
    # =========================================================

    def collect_source_ids(
        self,
        sources
    ):

        values = []

        for source in sources:

            source_id = self.clean(
                source.get(
                    "source_id"
                )
            )

            if source_id:

                values.append(
                    source_id
                )


        return list(
            dict.fromkeys(values)
        )


    # =========================================================
    # SOURCE URLS
    # =========================================================

    def collect_source_urls(
        self,
        sources
    ):

        values = []

        for source in sources:

            url = self.clean(
                source.get(
                    "url"
                )
            )

            if url:

                values.append(
                    url
                )


        return list(
            dict.fromkeys(values)
        )


    # =========================================================
    # BUILD ONE
    # =========================================================

    def build_record(
        self,
        candidate
    ):

        candidate_id = self.clean(
            candidate.get(
                "candidate_id"
            )
        )

        location_id = self.clean(
            candidate.get(
                "location_id"
            )
        )

        product_id = self.clean(
            candidate.get(
                "product_id"
            )
        )


        # -----------------------------------------------------
        # BLOCKED CANDIDATES
        # -----------------------------------------------------

        if candidate.get(
            "status"
        ) != "CANDIDATE":

            return {

                "candidate_id":
                    candidate_id,

                "status":
                    "BLOCKED",

                "reason":
                    "candidate_not_allowed",

                "product_id":
                    product_id,

                "partner":
                    candidate.get(
                        "partner"
                    ),

                "location_id":
                    location_id,

                "location_name":
                    candidate.get(
                        "location_name"
                    ),

                "local_data_available":
                    False,

                "source_count":
                    0,

                "verified_fact_count":
                    0,

                "publish_allowed":
                    False

            }


        # -----------------------------------------------------
        # VERIFIED SOURCES
        # -----------------------------------------------------

        sources = self.verified_local_sources(
            location_id,
            product_id
        )


        facts = self.collect_facts(
            sources
        )


        source_ids = self.collect_source_ids(
            sources
        )


        source_urls = self.collect_source_urls(
            sources
        )


        # -----------------------------------------------------
        # QUALITY
        #
        # Mindestens:
        # - 1 aktive lokale Quelle
        # - 2 verifizierte Fakten
        # - 1 echte URL
        # -----------------------------------------------------

        local_data_available = all([

            len(sources) >= 1,

            len(facts) >= 2,

            len(source_ids) >= 1,

            len(source_urls) >= 1

        ])


        return {

            "candidate_id":
                candidate_id,

            "status":
                (
                    "LOCAL_DATA_READY"
                    if local_data_available
                    else "LOCAL_DATA_MISSING"
                ),

            "product_id":
                product_id,

            "product_name":
                candidate.get(
                    "product_name"
                ),

            "partner":
                candidate.get(
                    "partner"
                ),

            "category":
                candidate.get(
                    "category"
                ),

            "silo":
                candidate.get(
                    "silo"
                ),

            "location_id":
                location_id,

            "location_name":
                candidate.get(
                    "location_name"
                ),

            "state":
                candidate.get(
                    "state"
                ),

            "wikidata_id":
                candidate.get(
                    "wikidata_id"
                ),

            "policy":
                candidate.get(
                    "policy",
                    {}
                ),

            "market_data":
                {

                    "verified_facts":
                        facts,

                    "source_ids":
                        source_ids,

                    "source_urls":
                        source_urls,

                    "source_count":
                        len(
                            sources
                        ),

                    "verified_fact_count":
                        len(
                            facts
                        )

                },

            "validation":
                {

                    "candidate_allowed":
                        True,

                    "local_data_available":
                        local_data_available,

                    "source_verified":
                        bool(
                            sources
                        )
                        and all(
                            source.get(
                                "source_verified"
                            )
                            is True
                            for source in sources
                        ),

                    "unique_content":
                        False,

                    "publish_allowed":
                        False

                },

            "sources":
                sources

        }


    # =========================================================
    # BUILD
    # =========================================================

    def build(self):

        matrix = self.load_json(
            self.candidate_file
        )


        candidates = (
            matrix.get(
                "candidates",
                []
            )
            or []
        )


        records = []


        for candidate in candidates:

            records.append(
                self.build_record(
                    candidate
                )
            )


        ready = [
            x
            for x in records
            if x.get(
                "status"
            )
            == "LOCAL_DATA_READY"
        ]


        missing = [
            x
            for x in records
            if x.get(
                "status"
            )
            == "LOCAL_DATA_MISSING"
        ]


        blocked = [
            x
            for x in records
            if x.get(
                "status"
            )
            == "BLOCKED"
        ]


        partner_stats = {}

        for record in records:

            partner = self.clean(
                record.get(
                    "partner"
                )
            ) or "unknown"

            partner_stats.setdefault(
                partner,
                {
                    "total": 0,
                    "local_data_ready": 0,
                    "local_data_missing": 0,
                    "blocked": 0
                }
            )


            partner_stats[
                partner
            ][
                "total"
            ] += 1


            if record.get(
                "status"
            ) == "LOCAL_DATA_READY":

                partner_stats[
                    partner
                ][
                    "local_data_ready"
                ] += 1


            elif record.get(
                "status"
            ) == "LOCAL_DATA_MISSING":

                partner_stats[
                    partner
                ][
                    "local_data_missing"
                ] += 1


            else:

                partner_stats[
                    partner
                ][
                    "blocked"
                ] += 1


        output = {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "geo_local_source_bridge",

            "version":
                "1.0",

            "status":
                "ACTIVE",

            "rules":
                {

                    "candidate_required":
                        True,

                    "official_local_source_required":
                        True,

                    "source_verified_required":
                        True,

                    "active_source_required":
                        True,

                    "minimum_verified_facts":
                        2,

                    "minimum_source_urls":
                        1,

                    "no_fabricated_local_data":
                        True,

                    "bridge_does_not_publish":
                        True

                },

            "summary":
                {

                    "records":
                        len(
                            records
                        ),

                    "local_data_ready":
                        len(
                            ready
                        ),

                    "local_data_missing":
                        len(
                            missing
                        ),

                    "blocked":
                        len(
                            blocked
                        ),

                    "published":
                        0

                },

            "partner_stats":
                partner_stats,

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
            "GEO LOCAL SOURCE BRIDGE CREATED"
        )

        print(
            "RECORDS:",
            len(
                records
            )
        )

        print(
            "LOCAL DATA READY:",
            len(
                ready
            )
        )

        print(
            "LOCAL DATA MISSING:",
            len(
                missing
            )
        )

        print(
            "BLOCKED:",
            len(
                blocked
            )
        )

        print(
            "PUBLISHED: 0"
        )


        for record in ready:

            print(
                "READY:",
                record.get(
                    "location_name"
                ),
                "|",
                record.get(
                    "product_id"
                ),
                "| SOURCES:",
                record.get(
                    "market_data",
                    {}
                ).get(
                    "source_count"
                ),
                "| FACTS:",
                record.get(
                    "market_data",
                    {}
                ).get(
                    "verified_fact_count"
                )
            )


        return output


if __name__ == "__main__":

    GeoLocalSourceBridge().build()
