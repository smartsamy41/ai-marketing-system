import imaplib
from email import message_from_bytes
from email.header import decode_header

from engine.secret_manager import SecretManager


class YahooReader:

    def __init__(self):

        s = SecretManager()

        self.email = s.get(
            "YAHOO_ACCOUNT_EMAIL"
        )

        self.password = s.get(
            "YAHOO_APP_PASSWORD"
        )


    def decode(self, value):

        if not value:
            return ""

        result = ""

        for part, encoding in decode_header(value):

            if isinstance(part, bytes):
                result += part.decode(
                    encoding or "utf-8",
                    errors="ignore"
                )

            else:
                result += part

        return result


    def fetch_latest(self, folder="Inbox", limit=10):

        mail = None

        try:

            mail = imaplib.IMAP4_SSL(
                "imap.mail.yahoo.com",
                993
            )

            mail.login(
                self.email,
                self.password
            )

            status, data = mail.select(folder)

            if status != "OK":
                return []


            status, messages = mail.search(
                None,
                "ALL"
            )


            ids = messages[0].split()[-limit:]

            results = []


            for num in reversed(ids):

                status, msg_data = mail.fetch(
                    num,
                    "(BODY.PEEK[HEADER])"
                )


                msg = message_from_bytes(
                    msg_data[0][1]
                )


                results.append(
                    {
                        "sender": self.decode(
                            msg.get("From")
                        ),
                        "subject": self.decode(
                            msg.get("Subject")
                        )
                    }
                )


            return results


        finally:

            if mail:

                try:
                    mail.logout()
                except:
                    pass
