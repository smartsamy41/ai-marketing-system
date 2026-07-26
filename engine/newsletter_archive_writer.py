from datetime import datetime


class NewsletterArchiveWriter:

    def __init__(self, sheets):

        self.sheets = sheets


    def save(self, mail, analysis):

        if analysis.get("status") != "KEEP":
            return False


        row = [

            mail.get(
                "email_id",
                ""
            ),

            analysis.get(
                "partner",
                ""
            ),

            mail.get(
                "sender",
                ""
            ),

            mail.get(
                "subject",
                ""
            ),

            mail.get(
                "received_date",
                datetime.utcnow().isoformat()
            ),

            analysis.get(
                "category",
                ""
            ),

            "AUTO_DETECTED",

            "FALSE",

            "AI_CONTENT_ANALYSIS",

            "ANALYZED",

            datetime.utcnow().isoformat()

        ]


        self.sheets.append(
            "partner_newsletter_archive",
            row
        )


        return True
