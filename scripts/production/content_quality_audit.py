import json
from pathlib import Path
from datetime import datetime, timezone


class ContentQualityAudit:

    def __init__(self):

        self.landing_dir = Path(
            "content_repository/landingpages/published"
        )

        self.article_dir = Path(
            "content_repository/articles/published"
        )

        self.report_file = Path(
            "data_master/logs/content_quality_audit_report.json"
        )


    def check_file(
        self,
        file_path,
        file_type
    ):

        result = {

            "file":
                str(file_path),

            "type":
                file_type,

            "checks":
                {},

            "score":
                0,

            "status":
                "FAILED"

        }


        if not file_path.exists():

            return result



        content = file_path.read_text(
            encoding="utf-8"
        )


        checks = {}



        if file_type == "landingpage":

            checks["title"] = (
                "<title>" in content
            )

            checks["description"] = (
                "description" in content
            )

            checks["schema"] = (
                "application/ld+json" in content
            )

            checks["faq"] = (
                "FAQ" in content
                or
                "Häufige Fragen" in content
            )

            checks["sources"] = (
                "Quellen" in content
                or
                "Fakten" in content
            )

            checks["advertising"] = (
                "Werbung / Anzeige" in content
            )

            checks["tracking"] = (
                "/track?" in content
            )

            checks["internal_links"] = (
                "related" in content
                or
                "interne" in content
            )



        if file_type == "article":

            checks["article_schema"] = (
                '"@type": "Article"' in content
            )

            checks["author"] = (
                '"author"' in content
            )

            checks["direct_answer"] = (
                "Direktantwort" in content
            )

            checks["facts"] = (
                "Fakten" in content
            )

            checks["sources"] = (
                "Quellen" in content
            )

            checks["faq"] = (
                "FAQ" in content
                or
                "Fragen und Antworten" in content
            )

            checks["related_content"] = (
                "Passende Themen" in content
                or
                "related" in content
            )



        passed = sum(
            1
            for value in checks.values()
            if value
        )


        total = len(checks)


        result["checks"] = checks

        result["score"] = (
            round(
                passed / total * 100
            )
            if total
            else 0
        )


        if result["score"] >= 80:

            result["status"] = "OK"


        return result



    def run(self):


        report = {


            "system":
                "FREE BASICS AI MARKETING SYSTEM",


            "type":
                "content_quality_audit",


            "created":
                datetime.now(
                    timezone.utc
                ).isoformat(),


            "landingpages":
                [],


            "articles":
                [],


            "summary":
                {}

        }



        landing_success = 0
        landing_failed = 0


        article_success = 0
        article_failed = 0



        for file in sorted(
            self.landing_dir.glob("*.html")
        ):

            result = self.check_file(
                file,
                "landingpage"
            )

            report["landingpages"].append(
                result
            )


            if result["status"] == "OK":

                landing_success += 1

            else:

                landing_failed += 1




        for file in sorted(
            self.article_dir.glob("*.html")
        ):

            result = self.check_file(
                file,
                "article"
            )

            report["articles"].append(
                result
            )


            if result["status"] == "OK":

                article_success += 1

            else:

                article_failed += 1



        report["summary"] = {


            "landingpages_ok":
                landing_success,


            "landingpages_failed":
                landing_failed,


            "articles_ok":
                article_success,


            "articles_failed":
                article_failed,


            "overall_status":
                "READY"
                if landing_failed == 0
                and article_failed == 0
                else "CHECK_REQUIRED"

        }



        self.report_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        with open(
            self.report_file,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(
                report,
                f,
                indent=2,
                ensure_ascii=False
            )


        print(
            "CONTENT QUALITY AUDIT FINISHED"
        )

        print(
            json.dumps(
                report["summary"],
                indent=2,
                ensure_ascii=False
            )
        )



if __name__ == "__main__":

    ContentQualityAudit().run()
