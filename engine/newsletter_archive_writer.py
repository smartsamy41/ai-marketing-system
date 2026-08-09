from datetime import datetime


class NewsletterArchiveWriter:


    SHEET_NAME = "partner_newsletter_archive"


    HEADERS = [
        "email_id",
        "partner",
        "sender",
        "subject",
        "received_date",
        "category",
        "campaign",
        "asset_found",
        "content_idea",
        "analysis_status",
        "created_at"
    ]



    def __init__(
        self,
        sheets
    ):

        self.sheets = sheets

        self.sheets.ensure_sheet(
            self.SHEET_NAME,
            self.HEADERS
        )



    def save(
        self,
        mail,
        analysis
    ):


        if analysis.get(
            "status"
        ) != "KEEP":

            return False



        row = [

            mail.get(
                "message_id",
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


            "PENDING_AI_ANALYSIS",


            "RAW_STORED",


            datetime.utcnow().isoformat()

        ]



        self.sheets.append(
            self.SHEET_NAME,
            row
        )


        return True
