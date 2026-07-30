import imaplib
import subprocess
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


mail = imaplib.IMAP4_SSL("imap.gmail.com")

mail.login(
    secret("GMAIL_ACCOUNT_EMAIL"),
    secret("GMAIL_APP_PASSWORD")
)

router = NewsletterMailRouter()

mail.select("INBOX")

status, data = mail.search(None, "ALL")

ids = data[0].split()[-20:]

print("GEPRÜFTE MAILS:", len(ids))


for num in ids:

    status, msg_data = mail.fetch(
        num,
        "(BODY.PEEK[HEADER])"
    )

    header = msg_data[0][1].decode(
        errors="ignore"
    )

    sender = ""
    subject = ""

    for line in header.splitlines():

        if line.lower().startswith("from:"):
            sender = line[5:]

        if line.lower().startswith("subject:"):
            subject = line[8:]


    result = router.route(
        {
            "sender": sender,
            "subject": subject
        }
    )

    if result["status"] == "MOVE":

        print(
            "MOVE:",
            sender,
            "->",
            result["folder"]
        )

    else:

        print(
            "IGNORE:",
            sender
        )


mail.logout()
