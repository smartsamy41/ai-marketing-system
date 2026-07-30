import imaplib
import subprocess
from email import message_from_bytes
from engine.newsletter_mail_router import NewsletterMailRouter


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


router = NewsletterMailRouter()


folders = [
    "Amazon_Newsletter",
    "Amazon_Partner",
    "Partner_Newsletter"
]


moved = 0


for folder in folders:

    print()
    print("ORDNER:", folder)

    mail.select(folder)

    _, data = mail.search(
        None,
        "ALL"
    )

    ids = data[0].split()

    print("MAILS:", len(ids))


    for num in ids:

        _, msg_data = mail.fetch(
            num,
            "(BODY.PEEK[HEADER])"
        )

        msg = message_from_bytes(
            msg_data[0][1]
        )

        mail_data = {
            "sender": msg.get("From",""),
            "subject": msg.get("Subject","")
        }


        result = router.route(mail_data)


        if result["status"] == "MOVE":

            target = result["folder"]

            print(
                "MOVE:",
                mail_data["sender"],
                "->",
                target
            )


            status, _ = mail.copy(
                num,
                f'"{target}"'
            )


            if status == "OK":

                mail.store(
                    num,
                    "+FLAGS",
                    "\\Deleted"
                )

                moved += 1


    mail.expunge()


print()
print("FERTIG")
print("VERSCHOBEN:", moved)

mail.logout()
