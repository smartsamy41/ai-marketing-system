from engine.gmail_reader import GmailReader
from engine.yahoo_reader import YahooReader
from engine.newsletter_filter import NewsletterFilter
from engine.newsletter_archive_writer import NewsletterArchiveWriter
from engine.newsletter_raw_storage import NewsletterRawStorage


class UnifiedMailScanner:


    def __init__(self, sheets):

        self.gmail = GmailReader()

        self.yahoo = YahooReader()

        self.filter = NewsletterFilter()

        self.raw_storage = NewsletterRawStorage()

        self.writer = NewsletterArchiveWriter(
            sheets
        )



    def process_mail(
        self,
        mail,
        source
    ):

        try:

            mail["source"] = source


            raw_result = self.raw_storage.save(
                mail
            )


            result = self.filter.analyze(
                mail
            )


            saved = False


            if result["status"] == "KEEP":

                saved = self.writer.save(
                    mail,
                    result
                )


            return {

                "status": "OK",

                "source": source,

                "raw_storage": raw_result,

                "saved": saved,

                "analysis": result,

                "mail": mail

            }


        except Exception as e:


            return {

                "status": "ERROR",

                "source": source,

                "error": str(e),

                "mail": mail

            }



    def scan_source(
        self,
        mails,
        source
    ):

        results = []

        total = len(mails)


        for index, mail in enumerate(
            mails,
            start=1
        ):

            print(
                f"[{source}] {index}/{total}",
                mail.get("subject","")
            )


            results.append(
                self.process_mail(
                    mail,
                    source
                )
            )


        return results



    def scan(self):

        results = []


        print(
            "=== NEWSLETTER SCAN START ==="
        )


        gmail_sources = [

            (
                "GMAIL:INBOX",
                self.gmail.fetch_from_folder(
                    "INBOX",
                    50
                )
            ),

            (
                "GMAIL:CHECK24",
                self.gmail.fetch_from_folder(
                    "Free Basics/Partner/Check24",
                    50
                )
            ),

            (
                "GMAIL:TARIFCHECK",
                self.gmail.fetch_from_folder(
                    "Free Basics/Partner/Tarifcheck",
                    50
                )
            ),

            (
                "GMAIL:TELEKOM",
                self.gmail.fetch_from_folder(
                    "Free Basics/Partner/Telekom",
                    50
                )
            )

        ]


        for source, mails in gmail_sources:

            results.extend(
                self.scan_source(
                    mails,
                    source
                )
            )



        yahoo_sources = [

            (
                "YAHOO:INBOX",
                self.yahoo.fetch_latest(
                    "Inbox",
                    50
                )
            ),

            (
                "YAHOO:AMAZON_PARTNER",
                self.yahoo.fetch_latest(
                    "Amazon_Partner",
                    50
                )
            ),

            (
                "YAHOO:AMAZON_NEWSLETTER",
                self.yahoo.fetch_latest(
                    "Amazon_Newsletter",
                    50
                )
            )

        ]


        for source, mails in yahoo_sources:

            results.extend(
                self.scan_source(
                    mails,
                    source
                )
            )


        print(
            "=== NEWSLETTER SCAN END ==="
        )

        print(
            "TOTAL:",
            len(results)
        )


        return results
