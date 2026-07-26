from engine.gmail_reader import GmailReader
from engine.yahoo_reader import YahooReader
from engine.newsletter_filter import NewsletterFilter
from engine.newsletter_archive_writer import NewsletterArchiveWriter


class UnifiedMailScanner:

    def __init__(self, sheets):

        self.gmail = GmailReader()
        self.yahoo = YahooReader()

        self.filter = NewsletterFilter()

        self.writer = NewsletterArchiveWriter(
            sheets
        )


    def process_mail(self, mail, source):

        mail["source"] = source

        result = self.filter.analyze(
            mail
        )

        if result["status"] == "KEEP":

            saved = self.writer.save(
                mail,
                result
            )

            return {
                "source": source,
                "saved": saved,
                "analysis": result,
                "mail": mail
            }


        return {
            "source": source,
            "saved": False,
            "analysis": result,
            "mail": mail
        }


    def scan(self):

        results = []


        # Gmail
        for mail in self.gmail.fetch_latest(50):

            results.append(
                self.process_mail(
                    mail,
                    "GMAIL"
                )
            )


        # Yahoo Inbox
        for mail in self.yahoo.fetch_latest(
            "Inbox",
            50
        ):

            results.append(
                self.process_mail(
                    mail,
                    "YAHOO"
                )
            )


        # Yahoo Affiliate
        for mail in self.yahoo.fetch_latest(
            "affiliate",
            50
        ):

            results.append(
                self.process_mail(
                    mail,
                    "YAHOO_AFFILIATE"
                )
            )


        return results
