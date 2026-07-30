from engine.gmail_reader import GmailReader
from engine.gmail_newsletter_router import GmailNewsletterRouter

reader = GmailReader()
router = NewsletterMailRouter()

mails = reader.fetch_latest(500)

stats = {}

print("GESAMT:", len(mails))
print("="*60)

for mail in mails:

    result = router.route(mail)

    if result["status"] == "MOVE":

        folder = result["folder"]

        stats[folder] = stats.get(folder, 0) + 1

        print(
            folder,
            "|",
            mail.get("sender"),
            "|",
            mail.get("subject")
        )


print()
print("="*60)
print("ZUSAMMENFASSUNG")

for k,v in stats.items():
    print(k, ":", v)

print("SCAN FERTIG")
