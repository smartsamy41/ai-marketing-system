from engine.google_sheets_live import GoogleSheetsLive


class NewsletterApprovalEngine:


    def __init__(self):

        self.sheets = GoogleSheetsLive()


    def get_partner_rule(
        self,
        partner
    ):

        rules = self.sheets.read_records(
            "newsletter_partner_rules"
        )


        for rule in rules:

            if (
                rule.get("partner","").lower()
                ==
                partner.lower()
            ):

                return rule


        return None



    def check(
        self,
        partner
    ):

        rule = self.get_partner_rule(
            partner
        )


        if not rule:

            return {
                "approval_required": True,
                "reason": "NO_RULE_FOUND"
            }


        required = (
            rule.get(
                "approval_required",
                "TRUE"
            )
            ==
            "TRUE"
        )


        return {
            "approval_required": required,
            "reason": rule.get(
                "template_source",
                ""
            ),
            "partner": partner
        }



    def approve(
        self,
        content_id
    ):

        records = self.sheets.read_records(
            "newsletter_content"
        )


        for row_number, record in enumerate(
            records,
            start=2
        ):

            if (
                record.get("content_id")
                ==
                content_id
            ):

                record["status"] = "APPROVED"


                self.sheets.update_row(
                    "newsletter_content",
                    row_number,
                    [
                        record.get("content_id",""),
                        record.get("campaign_id",""),
                        record.get("subject",""),
                        record.get("html",""),
                        record.get("status",""),
                        record.get("created_at",""),
                        record.get("updated_at","")
                    ]
                )


                return True


        return False
