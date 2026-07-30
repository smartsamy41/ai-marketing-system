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


folders = [
    "[Gmail]/All Mail",
    "[Gmail]/Alle Nachrichten",
    "[Gmail]/Spam",
    "[Gmail]/Papierkorb"
]


for folder in folders:

    print()
    print("TEST:", folder)

    mail = imaplib.IMAP4_SSL(
        "imap.gmail.com",
        993
    )

    mail.login(
        secret("GMAIL_ACCOUNT_EMAIL"),
        secret("GMAIL_APP_PASSWORD")
    )

    try:

        status, data = mail.select(folder)

        print(
            "STATUS:",
            status
        )

        if status == "OK":

            status, count = mail.search(
                None,
                "ALL"
            )

            print(
                "MAILS:",
                len(count[0].split())
            )

    except Exception as e:

        print(
            "FEHLER:",
            e
        )

    finally:
        mail.logout()
