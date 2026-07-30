import imaplib
import subprocess
from email import message_from_bytes
from email.header import decode_header


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


def decode(value):
    if not value:
        return ""

    result = ""

    for part, enc in decode_header(value):
        if isinstance(part, bytes):
            result += part.decode(
                enc or "utf-8",
                errors="ignore"
            )
        else:
            result += part

    return result


rules = {
    "Amazon": [
        "amazon",
        "partnernet",
        "kindle",
        "prime",
        "echo",
        "fire tv",
        "ads.amazon"
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


mail = imaplib.IMAP4_SSL(
    "imap.gmail.com"
)

mail.login(
    secret("GMAIL_ACCOUNT_EMAIL"),
    secret("GMAIL_APP_PASSWORD")
)

mail.select("INBOX")


status, data = mail.search(
    None,
    "ALL"
)

ids = data[0].split()

print("GESAMT MAILS:", len(ids))
print("="*60)


found = {}


for num in ids:

    try:

        status, msg_data = mail.fetch(
            num,
            "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])"
        )

        msg = message_from_bytes(
            msg_data[0][1]
        )

        sender = decode(
            msg.get("From")
        )

        subject = decode(
            msg.get("Subject")
        )

        text = (
            sender +
            " " +
            subject
        ).lower()


        for partner, keywords in rules.items():

            if any(
                k.lower() in text
                for k in keywords
            ):

                found.setdefault(
                    partner,
                    []
                ).append(
                    {
                        "sender": sender,
                        "subject": subject
                    }
                )

                break

    except Exception as e:
        print("Übersprungen:", num, e)


mail.logout()


for partner, mails in found.items():

    print()
    print("###", partner)
    print("ANZAHL:", len(mails))

    for m in mails[:10]:
        print("-", m["sender"])
        print(" ", m["subject"])


print()
print("SCAN FERTIG")
