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
    try:
        status, data = mail.delete(f'"{folder}"')

        print(
            folder,
            "DELETE:",
            status,
            data
        )

    except Exception as e:
        print(
            folder,
            "FEHLER:",
            e
        )


print("CLEANUP FERTIG")
