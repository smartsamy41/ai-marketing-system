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


labels = [

    # Partner Newsletter
    "Free Basics/Partner/Amazon",
    "Free Basics/Partner/Check24",
    "Free Basics/Partner/Tarifcheck",
    "Free Basics/Partner/Telekom",
    "Free Basics/Partner/Congstar",

    # Content Quellen
    "Free Basics/Content/Aktionen",
    "Free Basics/Content/Social Ideen",
    "Free Basics/Content/Blog Ideen",
    "Free Basics/Content/Werbemittel",

    # Eigene Newsletter Empfänger
    "Free Basics/Newsletter/DOI Pending",
    "Free Basics/Newsletter/Aktiv",
    "Free Basics/Newsletter/Abgemeldet",

]


for label in labels:

    try:
        result = mail.create(label)
        print(label, result[0])

    except Exception as e:
        print(label, "FEHLER", e)


mail.logout()

print("FERTIG")
