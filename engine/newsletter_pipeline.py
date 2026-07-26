from engine.newsletter_filter import NewsletterFilter
from engine.newsletter_mail_router import NewsletterMailRouter
from engine.newsletter_archive_writer import NewsletterArchiveWriter


class NewsletterPipeline:

    def __init__(self, sheets):

        self.filter = NewsletterFilter()
        self.router = NewsletterMailRouter()
        self.archive = NewsletterArchiveWriter(
            sheets
        )


    def process(self, mail):

        analysis = self.filter.analyze(
            mail
        )

        if analysis["status"] != "KEEP":

            return {
                "status": "IGNORE",
                "mail": mail
            }


        route = self.router.route(
            mail
        )


        saved = self.archive.save(
            mail,
            analysis
        )


        return {
            "status": "PROCESSED",
            "route": route,
            "saved": saved,
            "analysis": analysis
        }
