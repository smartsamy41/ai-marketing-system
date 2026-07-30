import imaplib
import email
import subprocess


class GmailReader:

    def __init__(self):
        self.email = self.secret("GMAIL_ACCOUNT_EMAIL")
        self.password = self.secret("GMAIL_APP_PASSWORD")


    def secret(self, name):

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


    def connect(self):

        mail = imaplib.IMAP4_SSL(
            "imap.gmail.com"
        )

        mail.login(
            self.email,
            self.password
        )

        return mail


    def decode_text(self, value):

        if not value:
            return ""

        decoded = email.header.decode_header(
            value
        )

        result = ""

        for part, encoding in decoded:

            if isinstance(part, bytes):

                result += part.decode(
                    encoding or "utf-8",
                    errors="ignore"
                )

            else:

                result += part

        return result


    def fetch_from_folder(
        self,
        folder,
        limit=10
    ):

        mail = self.connect()

        try:

            status, _ = mail.select(
                f'"{folder}"'
            )

            if status != "OK":
                return []


            _, data = mail.search(
                None,
                "ALL"
            )


            ids = data[0].split()[-limit:]


            messages = []


            for num in ids:

                _, msg_data = mail.fetch(
                    num,
                    "(RFC822)"
                )


                msg = email.message_from_bytes(
                    msg_data[0][1]
                )


                messages.append(
                    {
                        "sender":
                            msg.get("From",""),

                        "subject":
                            self.decode_text(
                                msg.get("Subject","")
                            ),

                        "folder":
                            folder
                    }
                )


            return messages


        finally:

            mail.logout()



    def fetch_latest(
        self,
        limit=10
    ):

        folders = [

            "Free Basics/Newsletter",

            "Partner",

            "Affiliate",

            "Newsletter",

            "INBOX"

        ]


        messages = []


        for folder in folders:

            messages.extend(
                self.fetch_from_folder(
                    folder,
                    limit
                )
            )


        return messages
