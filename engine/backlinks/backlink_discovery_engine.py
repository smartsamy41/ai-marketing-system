import json

from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

from adapters.research_and_wiki_adapters.web_backlink_crawler.backlink_analyzer import (
    BacklinkAnalyzer
)


class BacklinkDiscoveryEngine:

    DYNAMIC_PLATFORMS = {
        "youtube",
        "tiktok",
        "pinterest",
        "medium"

    }


    def __init__(self):

        self.candidate_file = Path(
            "data_master/authority_layer/backlink_candidates.json"
        )

        self.report_file = Path(
            "data_master/authority_layer/backlink_discovery_report.json"
        )

        self.registry_file = Path(
            "data_master/authority_layer/backlink_registry.json"
        )

        self.analyzer = BacklinkAnalyzer()


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
    def normalize_domain(url):

        try:

            parsed = urlparse(
                url
            )

            domain = parsed.netloc.lower()

            if domain.startswith(
                "www."
            ):

                domain = domain[4:]

            return domain

        except Exception:

            return ""


    @staticmethod
    def valid_http_url(url):

        try:

            parsed = urlparse(
                url
            )

            return (
                parsed.scheme in {
                    "http",
                    "https"
                }
                and bool(
                    parsed.netloc
                )
            )

        except Exception:

            return False


    # =========================================================
    # EMPTY REGISTRY
    # =========================================================

    def empty_candidate_registry(self):

        return {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "backlink_candidate_registry",

            "version":
                "2.0",

            "status":
                "ACTIVE",

            "rules":
                {

                    "candidate_is_not_backlink":
                        True,

                    "verification_required":
                        True,

                    "freebasics_link_required":
                        True,

                    "dynamic_platforms_need_special_handling":
                        True,

                    "no_artificial_backlinks":
                        True,

                    "no_fabricated_backlinks":
                        True,

                    "no_fabricated_metrics":
                        True

                },

            "summary":
                {

                    "total":
                        0,

                    "pending":
                        0,

                    "verified":
                        0,

                    "not_found_in_html":
                        0,

                    "dynamic_page_unverified":
                        0,

                    "errors":
                        0

                },

            "candidates":
                [],

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()
        }


    # =========================================================
    # LOAD / SAVE CANDIDATES
    # =========================================================

    def load_candidates(self):

        data = self.load_json(
            self.candidate_file
        )

        if data:
            return data

        data = self.empty_candidate_registry()

        self.save_json(
            self.candidate_file,
            data
        )

        return data


    def save_candidates(
        self,
        data
    ):

        candidates = (
            data.get(
                "candidates",
                []
            )
            or []
        )


        data[
            "summary"
        ] = {

            "total":
                len(
                    candidates
                ),

            "pending":
                sum(
                    1
                    for x in candidates
                    if x.get(
                        "status"
                    )
                    == "PENDING"
                ),

            "verified":
                sum(
                    1
                    for x in candidates
                    if x.get(
                        "status"
                    )
                    == "VERIFIED"
                ),

            "not_found_in_html":
                sum(
                    1
                    for x in candidates
                    if x.get(
                        "status"
                    )
                    == "NOT_FOUND_IN_HTML"
                ),

            "dynamic_page_unverified":
                sum(
                    1
                    for x in candidates
                    if x.get(
                        "status"
                    )
                    == "DYNAMIC_PAGE_UNVERIFIED"
                ),

            "errors":
                sum(
                    1
                    for x in candidates
                    if x.get(
                        "status"
                    )
                    == "ERROR"
                )
        }


        data[
            "updated_at"
        ] = datetime.now(
            timezone.utc
        ).isoformat()


        self.save_json(
            self.candidate_file,
            data
        )


    # =========================================================
    # ADD CANDIDATE
    # =========================================================

    def add_candidate(
        self,
        source_url,
        platform="",
        source_type="external_reference",
        discovery_source="manual",
        note=""
    ):

        source_url = self.clean(
            source_url
        )


        if not self.valid_http_url(
            source_url
        ):

            return {

                "status":
                    "INVALID_URL",

                "source_url":
                    source_url
            }


        if self.analyzer.is_freebasics_url(
            source_url
        ):

            return {

                "status":
                    "BLOCKED",

                "reason":
                    "SOURCE_IS_FREEBASICS",

                "source_url":
                    source_url
            }


        data = self.load_candidates()

        candidates = (
            data.get(
                "candidates",
                []
            )
            or []
        )


        for item in candidates:

            if self.clean(
                item.get(
                    "source_url"
                )
            ) == source_url:

                return {

                    "status":
                        "EXISTS",

                    "candidate":
                        item
                }


        now = datetime.now(
            timezone.utc
        ).isoformat()


        record = {

            "candidate_id":
                (
                    self.normalize_domain(
                        source_url
                    )
                    + "::"
                    + str(
                        len(
                            candidates
                        )
                        + 1
                    )
                ),

            "source_url":
                source_url,

            "source_domain":
                self.normalize_domain(
                    source_url
                ),

            "platform":
                self.clean(
                    platform
                ).lower(),

            "source_type":
                self.clean(
                    source_type
                )
                or "external_reference",

            "discovery_source":
                self.clean(
                    discovery_source
                )
                or "manual",

            "note":
                self.clean(
                    note
                ),

            "status":
                "PENDING",

            "backlink_found":
                False,

            "backlinks_found":
                0,

            "http_status":
                None,

            "first_discovered":
                now,

            "last_checked":
                None
        }


        candidates.append(
            record
        )


        data[
            "candidates"
        ] = candidates


        self.save_candidates(
            data
        )


        return {

            "status":
                "ADDED",

            "candidate":
                record
        }


    # =========================================================
    # VERIFY ONE
    # =========================================================

    def verify_candidate(
        self,
        candidate
    ):

        source_url = self.clean(
            candidate.get(
                "source_url"
            )
        )

        platform = self.clean(
            candidate.get(
                "platform"
            )
        ).lower()


        result = (
            self.analyzer.register_source(
                source_url=source_url,
                source_type=(
                    candidate.get(
                        "source_type"
                    )
                    or "external_reference"
                )
            )
        )


        now = datetime.now(
            timezone.utc
        ).isoformat()


        candidate[
            "last_checked"
        ] = now


        status = result.get(
            "status"
        )


        # =====================================================
        # VERIFIED
        # =====================================================

        if status == "REGISTERED":

            candidate[
                "status"
            ] = "VERIFIED"

            candidate[
                "backlink_found"
            ] = True

            candidate[
                "backlinks_found"
            ] = result.get(
                "backlinks_found",
                0
            )

            candidate[
                "verification_result"
            ] = result

            candidate.pop(
                "error",
                None
            )

            candidate.pop(
                "verification_note",
                None
            )


        # =====================================================
        # NOT FOUND
        # =====================================================

        elif status == "NOT_FOUND":

            candidate[
                "backlink_found"
            ] = False

            candidate[
                "backlinks_found"
            ] = 0

            candidate[
                "http_status"
            ] = result.get(
                "http_status"
            )


            if platform in self.DYNAMIC_PLATFORMS:

                candidate[
                    "status"
                ] = "DYNAMIC_PAGE_UNVERIFIED"

                candidate[
                    "verification_note"
                ] = (
                    "No Free Basics backlink was found "
                    "in the fetched HTML. "
                    "This platform may render profile "
                    "links dynamically."
                )

            else:

                candidate[
                    "status"
                ] = "NOT_FOUND_IN_HTML"

                candidate[
                    "verification_note"
                ] = (
                    "No Free Basics backlink was found "
                    "in the fetched HTML."
                )


            candidate.pop(
                "error",
                None
            )


        # =====================================================
        # ERROR
        # =====================================================

        elif status == "ERROR":

            candidate[
                "status"
            ] = "ERROR"

            candidate[
                "backlink_found"
            ] = False

            candidate[
                "backlinks_found"
            ] = 0

            candidate[
                "error"
            ] = result.get(
                "error",
                ""
            )


        # =====================================================
        # UNKNOWN
        # =====================================================

        else:

            candidate[
                "status"
            ] = "ERROR"

            candidate[
                "backlink_found"
            ] = False

            candidate[
                "error"
            ] = (
                "Unknown analyzer result: "
                + str(
                    status
                )
            )


        return candidate


    # =========================================================
    # VERIFY ALL
    # =========================================================

    def verify_all(
        self
    ):

        data = self.load_candidates()

        candidates = (
            data.get(
                "candidates",
                []
            )
            or []
        )


        results = []


        for candidate in candidates:

            results.append(
                self.verify_candidate(
                    candidate
                )
            )


        data[
            "candidates"
        ] = results


        self.save_candidates(
            data
        )


        report = self.build_report(
            results
        )


        self.save_json(
            self.report_file,
            report
        )


        summary = report.get(
            "summary",
            {}
        )


        print(
            "BACKLINK DISCOVERY COMPLETE V2"
        )

        print(
            "CANDIDATES:",
            summary.get(
                "candidates",
                0
            )
        )

        print(
            "VERIFIED:",
            summary.get(
                "verified",
                0
            )
        )

        print(
            "NOT FOUND IN HTML:",
            summary.get(
                "not_found_in_html",
                0
            )
        )

        print(
            "DYNAMIC UNVERIFIED:",
            summary.get(
                "dynamic_page_unverified",
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
            "REGISTRY:",
            self.registry_file
        )

        print(
            "REPORT:",
            self.report_file
        )


        return report


    # =========================================================
    # REPORT
    # =========================================================

    def build_report(
        self,
        candidates
    ):

        verified = [
            x
            for x in candidates
            if x.get(
                "status"
            )
            == "VERIFIED"
        ]

        not_found_in_html = [
            x
            for x in candidates
            if x.get(
                "status"
            )
            == "NOT_FOUND_IN_HTML"
        ]

        dynamic_unverified = [
            x
            for x in candidates
            if x.get(
                "status"
            )
            == "DYNAMIC_PAGE_UNVERIFIED"
        ]

        errors = [
            x
            for x in candidates
            if x.get(
                "status"
            )
            == "ERROR"
        ]


        return {

            "system":
                "FREE BASICS AI MARKETING SYSTEM",

            "type":
                "backlink_discovery_report",

            "version":
                "2.0",

            "status":
                "ACTIVE",

            "rules":
                {

                    "verified_backlinks_only":
                        True,

                    "candidate_not_equal_backlink":
                        True,

                    "dynamic_platforms_are_not_negative_proof":
                        True,

                    "no_artificial_backlinks":
                        True,

                    "no_fabricated_backlinks":
                        True
                },

            "summary":
                {

                    "candidates":
                        len(
                            candidates
                        ),

                    "verified":
                        len(
                            verified
                        ),

                    "not_found_in_html":
                        len(
                            not_found_in_html
                        ),

                    "dynamic_page_unverified":
                        len(
                            dynamic_unverified
                        ),

                    "errors":
                        len(
                            errors
                        )
                },

            "verified":
                [

                    {
                        "source_url":
                            x.get(
                                "source_url"
                            ),

                        "source_domain":
                            x.get(
                                "source_domain"
                            ),

                        "platform":
                            x.get(
                                "platform"
                            ),

                        "backlinks_found":
                            x.get(
                                "backlinks_found",
                                0
                            )
                    }

                    for x in verified
                ],

            "not_found_in_html":
                [
                    {
                        "source_url":
                            x.get(
                                "source_url"
                            ),

                        "platform":
                            x.get(
                                "platform"
                            )
                    }
                    for x in not_found_in_html
                ],

            "dynamic_page_unverified":
                [
                    {
                        "source_url":
                            x.get(
                                "source_url"
                            ),

                        "platform":
                            x.get(
                                "platform"
                            )
                    }
                    for x in dynamic_unverified
                ],

            "updated_at":
                datetime.now(
                    timezone.utc
                ).isoformat()
        }


    # =========================================================
    # RECHECK VERIFIED REGISTRY
    # =========================================================

    def recheck_registry(
        self
    ):

        return (
            self.analyzer.recheck_all()
        )


    # =========================================================
    # STATUS
    # =========================================================

    def status(
        self
    ):

        candidate_data = (
            self.load_candidates()
        )

        backlink_data = (
            self.analyzer.load_registry()
        )


        return {

            "candidate_summary":
                candidate_data.get(
                    "summary",
                    {}
                ),

            "backlink_summary":
                backlink_data.get(
                    "summary",
                    {}
                )
        }


# =============================================================
# DIRECT RUN
# =============================================================

if __name__ == "__main__":

    engine = BacklinkDiscoveryEngine()

    candidates = (
        engine.load_candidates()
    )

    registry = (
        engine.analyzer.load_registry()
    )


    print(
        "BACKLINK DISCOVERY ENGINE V2 READY"
    )

    print(
        "CANDIDATES:",
        candidates.get(
            "summary",
            {}
        ).get(
            "total",
            0
        )
    )

    print(
        "VERIFIED BACKLINKS:",
        registry.get(
            "summary",
            {}
        ).get(
            "active",
            0
        )
    )
