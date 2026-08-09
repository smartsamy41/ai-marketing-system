from datetime import datetime, timezone
import hashlib

from engine.google_sheets_live import GoogleSheetsLive
from engine.secret_manager import SecretManager


class NewsletterRawStorage:

    SHEET_NAME = "newsletter_raw_storage"

    HEADERS = [
        "message_id",
        "source",
        "folder",
        "partner",
        "sender",
        "subject",
        "received_date",
        "body_text",
        "body_html",
        "links",
        "attachments",
        "mail_hash",
        "processing_status",
        "created_at"
    ]


    def __init__(self):

        secrets = SecretManager()

        self.sheets = GoogleSheetsLive(
            spreadsheet_id=secrets.get(
                "GOOGLE_SHEET_ID"
            ),
            credentials_json=secrets.get(
                "GOOGLE_APPLICATION_CREDENTIALS_JSON"
            )
        )

        self.sheets.ensure_sheet(
            self.SHEET_NAME,
            self.HEADERS
        )

        # lokaler Cache für diese Scanner-Session
        self.hash_cache = set()

        self.cache_loaded = False



    def now(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def create_hash(self, mail):

        value = (
            mail.get("sender","")
            +
            mail.get("subject","")
            +
            mail.get("body_text","")
        )

        return hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()



    def load_cache_once(self):

        if self.cache_loaded:
            return

        records = self.sheets.read_records(
            self.SHEET_NAME
        )

        for row in records:

            h = row.get(
                "mail_hash",
                ""
            )

            if h:

                self.hash_cache.add(h)


        self.cache_loaded = True



    def limit_text(self, value):

        if not value:
            return ""

        return value[:20000]



    def exists(self, mail_hash):

        self.load_cache_once()

        return mail_hash in self.hash_cache



    def save(self, mail):

        mail_hash = self.create_hash(
            mail
        )


        if self.exists(
            mail_hash
        ):

            return {
                "status":"DUPLICATE",
                "mail_hash":mail_hash
            }



        self.sheets.append(
            self.SHEET_NAME,
            [

                mail.get("message_id",""),

                mail.get("source",""),

                mail.get("folder",""),

                mail.get("partner",""),

                mail.get("sender",""),

                mail.get("subject",""),

                mail.get("received_date",""),

                self.limit_text(
                    mail.get("body_text","")
                ),

                self.limit_text(
                    mail.get("body_html","")
                ),

                str(
                    mail.get("links",[])
                ),

                str(
                    mail.get("attachments",[])
                ),

                mail_hash,

                "RAW_STORED",

                self.now()

            ]
        )


        self.hash_cache.add(
            mail_hash
        )


        return {
            "status":"STORED",
            "mail_hash":mail_hash
        }
