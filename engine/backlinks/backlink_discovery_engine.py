import json

from pathlib import Path
from datetime import datetime, timezone


from adapters.research_and_wiki_adapters.web_backlink_crawler.backlink_analyzer import (
    BacklinkAnalyzer
)


class BacklinkDiscoveryEngine:


    DYNAMIC_PLATFORMS = {
        "youtube",
        "tiktok",
        "medium",
        "pinterest"
    }


    def __init__(self):

        self.candidate_file = Path(
            "data_master/authority_layer/backlink_candidates.json"
        )

        self.registry_file = Path(
            "data_master/authority_layer/backlink_registry.json"
        )

        self.report_file = Path(
            "data_master/authority_layer/backlink_discovery_report.json"
        )

        self.analyzer = BacklinkAnalyzer()



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



    def verify_candidate(self, candidate):


        result = self.analyzer.check_page(
            candidate["source_url"]
        )


        candidate["http_status"] = result.get(
            "http_status"
        )


        links = result.get(
            "links",
            []
        )


        candidate["backlinks_found"] = len(
            links
        )


        if links:


            candidate["status"] = "VERIFIED"

            candidate["backlink_found"] = True


        else:


            if candidate["platform"] in self.DYNAMIC_PLATFORMS:

                candidate["status"] = (
                    "DYNAMIC_PAGE_UNVERIFIED"
                )

            else:

                candidate["status"] = (
                    "NOT_FOUND_IN_HTML"
                )


            candidate["backlink_found"] = False



        candidate["last_checked"] = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )


        return candidate



    def verify_all(self):


        data = self.load_json(
            self.candidate_file
        )


        candidates = data.get(
            "candidates",
            []
        )


        registry = []


        for candidate in candidates:


            checked = self.verify_candidate(
                candidate
            )


            if checked["status"] == "VERIFIED":


                registry.append(

                    {

                        "source_domain":
                            checked["source_domain"],

                        "source_url":
                            checked["source_url"],

                        "target_url":
                            "https://freebasics.online",

                        "status":
                            "ACTIVE",

                        "follow":
                            True,

                        "nofollow":
                            False,

                        "links_found":
                            checked["backlinks_found"]

                    }

                )



        data["summary"] = {

            "total":
                len(candidates),

            "verified":
                sum(
                    1
                    for x in candidates
                    if x["status"]=="VERIFIED"
                ),

            "dynamic_page_unverified":
                sum(
                    1
                    for x in candidates
                    if x["status"]=="DYNAMIC_PAGE_UNVERIFIED"
                ),

            "not_found_in_html":
                sum(
                    1
                    for x in candidates
                    if x["status"]=="NOT_FOUND_IN_HTML"
                )

        }


        data["updated_at"] = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )


        self.save_json(
            self.candidate_file,
            data
        )


        self.save_json(

            self.registry_file,

            {

                "system":
                    "FREE BASICS AI MARKETING SYSTEM",

                "type":
                    "backlink_registry",

                "version":
                    "3.0",

                "summary":
                    {
                        "total": len(registry),
                        "active": len(registry)
                    },

                "backlinks":
                    registry

            }

        )


        self.save_json(

            self.report_file,

            {

                "system":
                    "FREE BASICS AI MARKETING SYSTEM",

                "type":
                    "backlink_discovery_report",

                "version":
                    "3.0",

                "summary":
                    data["summary"]

            }

        )


        print(
            "BACKLINK DISCOVERY COMPLETE V3"
        )

        print(
            "CANDIDATES:",
            len(candidates)
        )

        print(
            "VERIFIED:",
            data["summary"]["verified"]
        )

        print(
            "DYNAMIC:",
            data["summary"]["dynamic_page_unverified"]
        )

        print(
            "NOT FOUND:",
            data["summary"]["not_found_in_html"]
        )

        print(
            "REGISTRY:",
            self.registry_file
        )
