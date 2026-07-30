import imaplib
import subprocess


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

folders = [
    "INBOX",
    "[Gmail]/Alle Nachrichten",
    "Spam",
    "Papierkorb"
]


for folder in folders:

    print()
    print("ORDNER:", folder)

    try:

        mail.select(folder)

        status, data = mail.search(
            None,
            '(OR FROM "amazon" SUBJECT "Amazon")'
        )

        ids = data[0].split()

        print("AMAZON TREFFER:", len(ids))

    except Exception as e:

        print("FEHLER:", e)


mail.logout()
