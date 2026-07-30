from engine.yahoo_reader import YahooReader
from engine.newsletter_mail_router import NewsletterMailRouter


reader = YahooReader()
router = NewsletterMailRouter()


folders = [
    "Inbox",
    "affiliate",
    "Yahoo/Amazon",
    "Yahoo/Partnerprogramme"
]


for folder in folders:

    print()
    print("ORDNER:", folder)

    try:
        mails = reader.fetch_latest(
            folder,
            50
        )

        print("MAILS:", len(mails))

        for mail in mails:

            result = router.route(mail)

            if result["status"] == "MOVE":

                print(
                    result["folder"],
                    "|",
                    mail.get("sender"),
                    "|",
                    mail.get("subject")
                )

    except Exception as e:

        print("FEHLER:", e)

print("SCAN FERTIG")
