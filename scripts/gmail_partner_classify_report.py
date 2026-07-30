from engine.gmail_reader import GmailReader
from engine.mail_router import MailRouter

reader = GmailReader()
router = MailRouter()

mails = reader.fetch_latest(500)

print("GESAMT:", len(mails))
print("="*60)

for mail in mails:

    result = router.analyze(mail)

    if result["status"] == "RELEVANT":

        print("PARTNER:", result["partner"])
        print("FROM:", mail.get("sender"))
        print("SUBJECT:", mail.get("subject"))
        print("GRUND:", result["reason"])
        print("-"*60)
