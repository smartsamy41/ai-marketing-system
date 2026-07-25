import imaplib
import email
from email.header import decode_header
import subprocess


class GmailReader:

    def __init__(self):
        self.email = self.secret("GMAIL_ACCOUNT_EMAIL")
        self.password = self.secret("GMAIL_APP_PASSWORD")

    def secret(self, name):
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

    def fetch_latest(self, limit=5):

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.email, self.password)

        mail.select("INBOX")

        _, data = mail.search(None, "ALL")

        ids = data[0].split()[-limit:]

        messages = []

        for num in ids:
            _, msg_data = mail.fetch(num, "(RFC822)")

            msg = email.message_from_bytes(msg_data[0][1])

            sender = msg.get("From", "")
            subject = msg.get("Subject", "")

            messages.append({
                "sender": sender,
                "subject": subject
            })

        mail.logout()

        return messages
