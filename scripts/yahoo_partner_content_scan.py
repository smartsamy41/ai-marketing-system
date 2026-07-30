from engine.yahoo_reader import YahooReader
from engine.newsletter_mail_router import NewsletterMailRouter


reader = YahooReader()
router = NewsletterMailRouter()


folders = [
    "Amazon_Newsletter",
    "Amazon_Partner",
    "Partner_Newsletter"
]


for folder in folders:

    print()
    print("================")
    print("ORDNER:", folder)

    mails = reader.fetch_latest(
        folder,
        50
    )

    print("ANZAHL:", len(mails))


    for mail in mails:

        result = router.route(mail)

        print(
            result["status"],
            "|",
            result["folder"],
            "|",
            mail.get("sender"),
            "|",
            mail.get("subject")
        )


print()
print("SCAN FERTIG")
