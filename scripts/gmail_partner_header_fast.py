import imaplib
import subprocess
from email import message_from_bytes
from engine.gmail_newsletter_router import GmailNewsletterRouter


def secret(name):
    return subprocess.check_output(
        [
            "gcloud",
            "secrets",
            "versions",
            "access",
            "latest",
            "--secret="+name,
            "--project=smartcontent2050"
        ],
        text=True
    ).strip()


mail = imaplib.IMAP4_SSL(
    "imap.gmail.com",
    993
)

mail.login(
    secret("GMAIL_ACCOUNT_EMAIL"),
    secret("GMAIL_APP_PASSWORD")
)

mail.select("INBOX")

status, data = mail.search(None, "ALL")

ids = data[0].split()

print("GESAMT MAIL IDS:", len(ids))

router = GmailNewsletterRouter()

stats = {}

for num in ids[-352:]:

    status, msg_data = mail.fetch(
        num,
        "(BODY.PEEK[HEADER])"
    )

    msg = message_from_bytes(
        msg_data[0][1]
    )

    mail_data = {
        "sender": msg.get("From",""),
        "subject": msg.get("Subject","")
    }

    result = router.route(mail_data)

    if result["status"] == "MOVE":

        folder = result["folder"]

        stats[folder] = stats.get(folder,0)+1

        print(
            folder,
            "|",
            mail_data["sender"],
            "|",
            mail_data["subject"]
        )


print("====================")
print("ERGEBNIS")

for k,v in stats.items():
    print(k,":",v)

print("SCAN FERTIG")

mail.logout()
