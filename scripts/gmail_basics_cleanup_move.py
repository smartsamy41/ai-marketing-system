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


mail = imaplib.IMAP4_SSL("imap.gmail.com")

mail.login(
    secret("GMAIL_ACCOUNT_EMAIL"),
    secret("GMAIL_APP_PASSWORD")
)


folders = [
    "Basics/Partner/Amazon",
    "Basics/Partner/Check24",
    "Basics/Partner/Tarifcheck",
    "Basics/Partner/Telekom"
]


for folder in folders:

    print("\nPRÜFE:", folder)

    mail.select(f'"{folder}"')

    status, data = mail.search(None, "ALL")

    ids = data[0].split()

    print("VORHANDEN:", len(ids))

    for num in ids:
        mail.store(
            num,
            "+FLAGS",
            "\\Deleted"
        )

    mail.expunge()

    print("BEREINIGT:", folder)


print("\nCLEANUP FERTIG")
