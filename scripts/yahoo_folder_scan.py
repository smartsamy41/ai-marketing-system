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
    "imap.mail.yahoo.com",
    993
)

mail.login(
    secret("YAHOO_ACCOUNT_EMAIL"),
    secret("YAHOO_APP_PASSWORD")
)


status, folders = mail.list()

print("YAHOO ORDNER")
print("================")

for folder in folders:
    print(folder.decode())


mail.logout()
