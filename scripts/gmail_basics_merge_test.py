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


mapping = {
    "Basics/Partner/Amazon": "Free Basics/Partner/Amazon",
    "Basics/Partner/Check24": "Free Basics/Partner/Check24",
    "Basics/Partner/Tarifcheck": "Free Basics/Partner/Tarifcheck",
    "Basics/Partner/Telekom": "Free Basics/Partner/Telekom"
}


for source, target in mapping.items():

    print("\nSOURCE:", source)
    print("TARGET:", target)

    mail.select(f'"{source}"')

    status, data = mail.search(None, "ALL")

    ids = data[0].split()

    print("MAILS:", len(ids))

    for num in ids:

        status, _ = mail.copy(
            num,
            f'"{target}"'
        )

        print("COPIED:", num.decode())


print("\nMERGE COPY FERTIG")
