import imaplib
import subprocess
import email


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


folders = [
    "INBOX",
    "Free Basics/Newsletter",
    "Free Basics/Partner",
    "Partner",
    "Affiliate",
    "Newsletter",
    "[Gmail]/Spam",
    "[Gmail]/Papierkorb",
    "[Gmail]/Alle Nachrichten"
]


keywords = {
    "Amazon": [
        "amazon",
        "kindle",
        "partnernet",
        "associates"
    ],
    "Check24": [
        "check24"
    ],
    "Tarifcheck": [
        "tarifcheck"
    ],
    "Telekom": [
        "telekom",
        "telekom-profis"
    ],
    "Congstar": [
        "congstar"
    ]
}


for folder in folders:

    print("\nORDNER:", folder)

    try:
        mail.select(folder)

        status, data = mail.search(
            None,
            "ALL"
        )

        ids = data[0].split()

        print("MAILS:", len(ids))

        for num in ids[-20:]:

            status, msg_data = mail.fetch(
                num,
                "(RFC822)"
            )

            msg = email.message_from_bytes(
                msg_data[0][1]
            )

            sender = str(
                msg.get("From","")
            ).lower()

            subject = str(
                msg.get("Subject","")
            ).lower()

            text = sender + " " + subject

            for partner, words in keywords.items():

                if any(
                    w in text
                    for w in words
                ):
                    print(
                        partner,
                        "|",
                        msg.get("Subject",""),
                        "|",
                        msg.get("From","")
                    )

    except Exception as e:
        print("FEHLER:", e)


mail.logout()
