import imaplib
import subprocess
from email import message_from_bytes


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


folders = [
    "[Gmail]/Spam",
    "[Gmail]/Papierkorb"
]


for folder in folders:

    mail = imaplib.IMAP4_SSL(
        "imap.gmail.com",
        993
    )

    mail.login(
        secret("GMAIL_ACCOUNT_EMAIL"),
        secret("GMAIL_APP_PASSWORD")
    )

    print()
    print("ORDNER:", folder)

    mail.select(folder)

    _, data = mail.search(None, "ALL")

    ids = data[0].split()

    print("ANZAHL:", len(ids))

    for num in ids[-20:]:

        _, msg_data = mail.fetch(
            num,
            "(BODY.PEEK[HEADER])"
        )

        msg = message_from_bytes(
            msg_data[0][1]
        )

        print(
            msg.get("From",""),
            "|",
            msg.get("Subject","")
        )

    mail.logout()
