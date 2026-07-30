import imaplib
import subprocess

email_account = subprocess.check_output(
    [
        "gcloud",
        "secrets",
        "versions",
        "access",
        "latest",
        "--secret=GMAIL_ACCOUNT_EMAIL",
        "--project=smartcontent2050"
    ],
    text=True
).strip()

password = subprocess.check_output(
    [
        "gcloud",
        "secrets",
        "versions",
        "access",
        "latest",
        "--secret=GMAIL_APP_PASSWORD",
        "--project=smartcontent2050"
    ],
    text=True
).strip()


mail = imaplib.IMAP4_SSL("imap.gmail.com")

mail.login(
    email_account,
    password
)

status, folders = mail.list()

print("GMAIL LABELS:")
for folder in folders:
    print(folder.decode())

mail.logout()
