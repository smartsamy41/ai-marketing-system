import imaplib
from email import message_from_bytes

from engine.secret_manager import SecretManager
from engine.newsletter_mail_router import NewsletterMailRouter


class YahooMailMover:


    def __init__(self):

        s = SecretManager()

        self.email = s.get(
            "YAHOO_ACCOUNT_EMAIL"
        )

        self.password = s.get(
            "YAHOO_APP_PASSWORD"
        )

        self.router = NewsletterMailRouter()



    def connect(self):

        mail = imaplib.IMAP4_SSL(
            "imap.mail.yahoo.com",
            993
        )

        mail.login(
            self.email,
            self.password
        )

        return mail



    def move(
        self,
        folder="Inbox",
        limit=20
    ):

        mail = self.connect()

        mail.select(
            folder
        )


        status, data = mail.search(
            None,
            "ALL"
        )


        if status != "OK":

            mail.logout()

            return []



        ids = data[0].split()

        moved = []



        for mail_id in reversed(ids[-limit:]):


            status, msg_data = mail.fetch(
                mail_id,
                "(RFC822)"
            )


            if status != "OK":

                continue



            raw = msg_data[0][1]


            msg = message_from_bytes(
                raw
            )


            sender = msg.get(
                "From",
                ""
            )


            subject = msg.get(
                "Subject",
                ""
            )



            result = self.router.route(
                {
                    "sender": sender,
                    "subject": subject
                }
            )



            if result["status"] == "MOVE":


                target = result["folder"]


                mail.copy(
                    mail_id,
                    target
                )


                mail.store(
                    mail_id,
                    "+FLAGS",
                    "\\Deleted"
                )


                moved.append(
                    {
                        "from": sender,
                        "subject": subject,
                        "folder": target
                    }
                )



        mail.expunge()

        mail.logout()


        return moved
