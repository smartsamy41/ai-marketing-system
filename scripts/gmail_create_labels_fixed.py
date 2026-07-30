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
    "imap.gmail.com"
)

mail.login(
    secret("GMAIL_ACCOUNT_EMAIL"),
    secret("GMAIL_APP_PASSWORD")
)


labels = [
    "Free Basics/Partner",
    "Free Basics/Content",
    "Free Basics/Kunden Newsletter",
    "Free Basics/Archiv"
]


for label in labels:
    try:
        status, data = mail.create(label)
        print(label, status, data)

    except Exception as e:
        print(label, "FEHLER:", e)


mail.logout()

print("FERTIG")
