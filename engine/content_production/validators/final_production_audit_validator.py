import json
from pathlib import Path
from datetime import datetime, timezone


class FinalProductionAuditValidator:


    def __init__(self):

        self.html_path = Path(
            "data_master/content_production/final_pages"
        )

        self.schema_path = Path(
            "data_master/content_production/schema_output"
        )

        self.opengraph_path = Path(
            "data_master/content_production/opengraph_output"
        )

        self.output = Path(
            "data_master/content_production/final_audit"
        )



    def check_text(self, html, text):

        return text.lower() in html.lower()



    def validate_page(self, html_file):


        html = html_file.read_text(
            encoding="utf-8"
        )


        product_id = html_file.stem


        result = {


            "product_id":
            product_id,


            "html_exists":
            True,


            "checks":
            {

                "html":
                True,


                "affiliate_area":
                self.check_text(
                    html,
                    "affiliate"
                ),


                "advertising_label":
                (
                    self.check_text(
                        html,
                        "werbung"
                    )
                    or
                    self.check_text(
                        html,
                        "anzeige"
                    )
                ),


                "footer":
                self.check_text(
                    html,
                    "footer"
                ),


                "semantic_structure":
                (
                    self.check_text(
                        html,
                        "<main"
                    )
                    and
                    self.check_text(
                        html,
                        "<header"
                    )
                    and
                    self.check_text(
                        html,
                        "<footer"
                    )
                )

            }

        }



        result["status"] = (

            "PASS"

            if all(
                result["checks"].values()
            )

            else

            "REVIEW"

        )


        return result



    def build(self):


        self.output.mkdir(
            parents=True,
            exist_ok=True
        )


        reports=[]


        html_files = list(
            self.html_path.glob(
                "*.html"
            )
        )


        for html_file in html_files:


            reports.append(

                self.validate_page(
                    html_file
                )

            )



        summary = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "type":
            "final_production_audit",


            "created":
            datetime.now(
                timezone.utc
            ).isoformat(),


            "pages_checked":
            len(reports),


            "passed":
            len(
                [
                    x for x in reports
                    if x["status"]=="PASS"
                ]
            ),


            "review":
            len(
                [
                    x for x in reports
                    if x["status"]=="REVIEW"
                ]
            ),


            "pages":
            reports

        }



        with open(

            self.output /
            "final_production_audit.json",

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                summary,

                f,

                indent=2,

                ensure_ascii=False

            )


        print(
            "FINAL PRODUCTION AUDIT CREATED"
        )

        print(
            "PAGES CHECKED:",
            summary["pages_checked"]
        )

        print(
            "PASSED:",
            summary["passed"]
        )

        print(
            "REVIEW:",
            summary["review"]
        )



if __name__ == "__main__":

    FinalProductionAuditValidator().build()
