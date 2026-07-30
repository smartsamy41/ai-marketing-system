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

router = GmailNewsletterRouter()

_, data = mail.search(None, "ALL")

ids = data[0].split()

moved = 0

for num in ids:

    _, msg_data = mail.fetch(
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

        label = result["folder"]

        print(
            "LABEL:",
            label,
            "|",
            mail_data["sender"],
            "|",
            mail_data["subject"]
        )

        mail.store(
            num,
            "+X-GM-LABELS",
            label
        )

        moved += 1


print()
print("FERTIG")
print("LABELS GESETZT:", moved)

mail.logout()
