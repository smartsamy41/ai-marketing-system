import json
import runpy

from pathlib import Path
from datetime import datetime, timezone

from engine.landingpage_validator import (
    LandingpageValidator
)

from engine.content_intelligence.geo_page_renderer import (
    GeoPageRenderer
)

from engine.geo.geo_llms_manifest_builder import (
    GeoLlmsManifestBuilder
)

from engine.geo.geo_candidate_matrix_builder import (
    GeoCandidateMatrixBuilder
)

from engine.geo.geo_local_source_bridge import (
    GeoLocalSourceBridge
)

from engine.geo.geo_ready_candidate_processor import (
    GeoReadyCandidateProcessor
)


class GeoBatchOrchestrator:

    def __init__(self):

        self.nodes_file = Path(
            "data_master/geo_layer/geo_content_nodes.json"
        )

        self.output_file = Path(
            "data_master/geo_layer/geo_batch_report.json"
        )

        self.sitemap_script = Path(
            "scripts/production/generate_sitemap.py"
        )

        self.validator = LandingpageValidator()

        self.renderer = GeoPageRenderer()

        self.llms_builder = (
            GeoLlmsManifestBuilder()
        )

        self.candidate_builder = (
            GeoCandidateMatrixBuilder()
        )

        self.source_bridge = (
            GeoLocalSourceBridge()
        )

        self.ready_processor = (
            GeoReadyCandidateProcessor()
        )


    # =========================================================
    # JSON
    # =========================================================

    @staticmethod
    def load_json(
        path
    ):

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
    # PRE-PUBLISH PIPELINE
    # =========================================================

    def build_candidate_matrix(
        self
    ):

        try:

            result = (
                self.candidate_builder.build()
            )

            summary = (
                result.get(
                    "summary",
                    {}
                )
                or {}
            )

            return {
                "status": "UPDATED",
                "matrix_size":
                    summary.get(
                        "matrix_size",
                        0
                    ),
                "candidates":
                    summary.get(
                        "candidates",
                        0
                    ),
                "blocked":
                    summary.get(
                        "blocked",
                        0
                    )
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "error": str(error)
            }


    def build_local_source_bridge(
        self
    ):

        try:

            result = (
                self.source_bridge.build()
            )

            summary = (
                result.get(
                    "summary",
                    {}
                )
                or {}
            )

            return {
                "status": "UPDATED",
                "records":
                    summary.get(
                        "records",
                        0
                    ),
                "local_data_ready":
                    summary.get(
                        "local_data_ready",
                        0
                    ),
                "local_data_missing":
                    summary.get(
                        "local_data_missing",
                        0
                    ),
                "blocked":
                    summary.get(
                        "blocked",
                        0
                    )
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "error": str(error)
            }


    def build_ready_candidates(
        self
    ):

        try:

            result = (
                self.ready_processor.build()
            )

            summary = (
                result.get(
                    "summary",
                    {}
                )
                or {}
            )

            return {
                "status": "UPDATED",
                "local_data_ready_input":
                    summary.get(
                        "local_data_ready_input",
                        0
                    ),
                "ready_for_geo_validation":
                    summary.get(
                        "ready_for_geo_validation",
                        0
                    ),
                "blocked":
                    summary.get(
                        "blocked",
                        0
                    ),
                "errors":
                    summary.get(
                        "errors",
                        0
                    )
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "error": str(error)
            }


    # =========================================================
    # VALIDATOR INPUT
    # =========================================================

    @staticmethod
    def validator_page(
        node
    ):

        validation = (
            node.get(
                "validation",
                {}
            )
            or {}
        )

        return {

            "product_id":
                node.get(
                    "product_id"
                ),

            "page_type":
                "geo",

            "location_id":
                node.get(
                    "location_id"
                ),

            "location_name":
                node.get(
                    "location_name"
                ),

            "real_location":
                validation.get(
                    "real_location"
                ),

            "source_verified":
                validation.get(
                    "source_verified"
                ),

            "wikidata_verified":
                validation.get(
                    "wikidata_verified"
                ),

            "product_match":
                validation.get(
                    "product_match"
                ),

            "category_match":
                validation.get(
                    "category_match"
                ),

            "search_intent_match":
                validation.get(
                    "search_intent_match"
                ),

            "local_data_available":
                validation.get(
                    "local_data_available"
                ),

            "partner_compliant":
                validation.get(
                    "partner_compliant"
                ),

            "unique_content":
                validation.get(
                    "unique_content"
                )
        }


    # =========================================================
    # PROCESS SINGLE NODE
    # =========================================================

    def process_node(
        self,
        node
    ):

        product_id = str(
            node.get(
                "product_id",
                ""
            )
            or ""
        ).strip()

        location_id = str(
            node.get(
                "location_id",
                ""
            )
            or ""
        ).strip()

        partner = str(
            node.get(
                "partner",
                ""
            )
            or ""
        ).strip()


        if not product_id:

            return {
                "status": "BLOCKED",
                "reason": "MISSING_PRODUCT_ID"
            }


        if not location_id:

            return {
                "status": "BLOCKED",
                "product_id": product_id,
                "reason": "MISSING_LOCATION_ID"
            }


        page = self.validator_page(
            node
        )


        validation_result = (
            self.validator.validate(
                page,
                partner=partner
            )
        )


        allowed = all([

            validation_result.get(
                "status"
            )
            == "COMPLIANT",

            validation_result.get(
                "geo_quality_status"
            )
            == "INDEX",

            validation_result.get(
                "geo_publish_allowed"
            )
            is True,

            validation_result.get(
                "sitemap_allowed"
            )
            is True,

            validation_result.get(
                "llms_allowed"
            )
            is True

        ])


        if not allowed:

            return {

                "status":
                    "BLOCKED",

                "product_id":
                    product_id,

                "location_id":
                    location_id,

                "location_name":
                    node.get(
                        "location_name"
                    ),

                "partner":
                    partner,

                "validation":
                    validation_result
            }


        publish_result = (
            self.renderer.publish(
                product_id,
                location_id
            )
        )


        publish_status = (
            publish_result.get(
                "status",
                "ERROR"
            )
        )


        return {

            "status":
                (
                    "PUBLISHED"
                    if publish_status
                    == "PUBLISHED"
                    else publish_status
                ),

            "product_id":
                product_id,

            "location_id":
                location_id,

            "location_name":
                node.get(
                    "location_name"
                ),

            "partner":
                partner,

            "canonical_url":
                node.get(
                    "canonical_url"
                ),

            "validation":
                validation_result,

            "publishing":
                publish_result
        }


    # =========================================================
    # SITEMAP
    # =========================================================

    def rebuild_sitemap(
        self
    ):

        if not self.sitemap_script.exists():

            return {
                "status": "SKIPPED",
                "reason": "SITEMAP_SCRIPT_NOT_FOUND"
            }


        try:

            runpy.run_path(
                str(
                    self.sitemap_script
                ),
                run_name="__main__"
            )

            return {
                "status": "UPDATED"
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "error": str(error)
            }


    # =========================================================
    # LLMS
    # =========================================================

    def rebuild_llms(
        self
    ):

        try:

            result = (
                self.llms_builder.build()
            )

            return {

                "status":
                    result.get(
                        "status",
                        "UPDATED"
                    ),

                "geo_nodes":
                    result.get(
                        "geo_nodes",
                        0
                    ),

                "llms":
                    result.get(
                        "llms"
                    ),

                "llms_full":
                    result.get(
                        "llms_full"
                    )
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "error": str(error)
            }


    # =========================================================
    # REPORT
    # =========================================================

    def build_report(
        self,
        nodes,
        results,
        candidate_result,
        source_bridge_result,
        ready_result,
        product_id=None,
        limit=None,
        sitemap_result=None,
        llms_result=None
    ):

        published = [
            result
            for result in results
            if result.get(
                "status"
            )
            == "PUBLISHED"
        ]

        blocked = [
            result
            for result in results
            if result.get(
                "status"
            )
            == "BLOCKED"
        ]

        errors = [
            result
            for result in results
            if result.get(
                "status"
            )
            == "ERROR"
        ]


        return {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "geo_batch_report",

            "version":
                "3.0",

            "created":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "filter":
                {
                    "product_id":
                        product_id,

                    "limit":
                        limit
                },

            "pipeline":
                {

                    "candidate_matrix":
                        candidate_result,

                    "local_source_bridge":
                        source_bridge_result,

                    "ready_candidate_processor":
                        ready_result
                },

            "summary":
                {

                    "nodes_found":
                        len(
                            nodes
                        ),

                    "published":
                        len(
                            published
                        ),

                    "blocked":
                        len(
                            blocked
                        ),

                    "errors":
                        len(
                            errors
                        )
                },

            "sitemap":
                sitemap_result
                or {
                    "status":
                        "PENDING"
                },

            "llms":
                llms_result
                or {
                    "status":
                        "PENDING"
                },

            "results":
                results
        }


    # =========================================================
    # RUN
    # =========================================================

    def run(
        self,
        product_id=None,
        limit=None
    ):

        # =====================================================
        # STEP 1
        # CANDIDATE MATRIX
        # =====================================================

        candidate_result = (
            self.build_candidate_matrix()
        )

        if candidate_result.get(
            "status"
        ) == "ERROR":

            return {
                "status": "ERROR",
                "stage": "candidate_matrix",
                "result": candidate_result
            }


        # =====================================================
        # STEP 2
        # LOCAL SOURCES
        # =====================================================

        source_bridge_result = (
            self.build_local_source_bridge()
        )

        if source_bridge_result.get(
            "status"
        ) == "ERROR":

            return {
                "status": "ERROR",
                "stage": "local_source_bridge",
                "result": source_bridge_result
            }


        # =====================================================
        # STEP 3
        # MARKET + CONTENT NODES
        # =====================================================

        ready_result = (
            self.build_ready_candidates()
        )

        if ready_result.get(
            "status"
        ) == "ERROR":

            return {
                "status": "ERROR",
                "stage": "ready_candidate_processor",
                "result": ready_result
            }


        # =====================================================
        # STEP 4
        # LOAD RESULTING CONTENT NODES
        # =====================================================

        data = self.load_json(
            self.nodes_file
        )

        nodes = (
            data.get(
                "nodes",
                []
            )
            or []
        )


        if product_id:

            nodes = [
                node
                for node in nodes
                if str(
                    node.get(
                        "product_id",
                        ""
                    )
                )
                == str(
                    product_id
                )
            ]


        if limit is not None:

            nodes = nodes[
                :int(limit)
            ]


        # =====================================================
        # STEP 5
        # QUALITY SHIELD + PUBLISH
        # =====================================================

        results = []


        for node in nodes:

            try:

                result = (
                    self.process_node(
                        node
                    )
                )

            except Exception as error:

                result = {

                    "status":
                        "ERROR",

                    "product_id":
                        node.get(
                            "product_id"
                        ),

                    "location_id":
                        node.get(
                            "location_id"
                        ),

                    "location_name":
                        node.get(
                            "location_name"
                        ),

                    "error":
                        str(error)
                }


            results.append(
                result
            )


        published = [
            result
            for result in results
            if result.get(
                "status"
            )
            == "PUBLISHED"
        ]


        # =====================================================
        # STEP 6
        # SITEMAP
        # =====================================================

        if published:

            sitemap_result = (
                self.rebuild_sitemap()
            )

        else:

            sitemap_result = {
                "status": "SKIPPED",
                "reason": "NO_PUBLISHED_NODES"
            }


        # =====================================================
        # STEP 7
        # PRELIMINARY REPORT
        #
        # LLMS Builder liest diesen Report.
        # =====================================================

        preliminary_report = (
            self.build_report(

                nodes=nodes,

                results=results,

                candidate_result=candidate_result,

                source_bridge_result=source_bridge_result,

                ready_result=ready_result,

                product_id=product_id,

                limit=limit,

                sitemap_result=sitemap_result,

                llms_result={
                    "status": "PENDING"
                }
            )
        )


        self.save_json(
            self.output_file,
            preliminary_report
        )


        # =====================================================
        # STEP 8
        # LLMS
        # =====================================================

        if published:

            llms_result = (
                self.rebuild_llms()
            )

        else:

            llms_result = {

                "status":
                    "SKIPPED",

                "reason":
                    "NO_PUBLISHED_NODES",

                "geo_nodes":
                    0
            }


        # =====================================================
        # STEP 9
        # FINAL REPORT
        # =====================================================

        final_report = (
            self.build_report(

                nodes=nodes,

                results=results,

                candidate_result=candidate_result,

                source_bridge_result=source_bridge_result,

                ready_result=ready_result,

                product_id=product_id,

                limit=limit,

                sitemap_result=sitemap_result,

                llms_result=llms_result
            )
        )


        self.save_json(
            self.output_file,
            final_report
        )


        # =====================================================
        # OUTPUT
        # =====================================================

        summary = (
            final_report.get(
                "summary",
                {}
            )
            or {}
        )


        print()
        print(
            "========================================"
        )

        print(
            "FREE BASICS GEO PIPELINE COMPLETE V3"
        )

        print(
            "========================================"
        )

        print(
            "MATRIX:",
            candidate_result.get(
                "matrix_size",
                0
            )
        )

        print(
            "CANDIDATES:",
            candidate_result.get(
                "candidates",
                0
            )
        )

        print(
            "LOCAL DATA READY:",
            source_bridge_result.get(
                "local_data_ready",
                0
            )
        )

        print(
            "READY FOR GEO VALIDATION:",
            ready_result.get(
                "ready_for_geo_validation",
                0
            )
        )

        print(
            "NODES:",
            summary.get(
                "nodes_found",
                0
            )
        )

        print(
            "PUBLISHED:",
            summary.get(
                "published",
                0
            )
        )

        print(
            "BLOCKED:",
            summary.get(
                "blocked",
                0
            )
        )

        print(
            "ERRORS:",
            summary.get(
                "errors",
                0
            )
        )

        print(
            "SITEMAP:",
            sitemap_result.get(
                "status"
            )
        )

        print(
            "LLMS:",
            llms_result.get(
                "status"
            )
        )

        print(
            "LLMS GEO NODES:",
            llms_result.get(
                "geo_nodes",
                0
            )
        )

        print(
            "REPORT:",
            self.output_file
        )


        return final_report


if __name__ == "__main__":

    GeoBatchOrchestrator().run()
