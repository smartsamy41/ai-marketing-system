import imaplib
from email import message_from_bytes
from email.header import decode_header
from email.utils import parsedate_to_datetime
import re

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



    def decode(
        self,
        value
    ):

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



    def extract_body(
        self,
        msg
    ):

        body_text = ""
        body_html = ""


        if msg.is_multipart():

            for part in msg.walk():

                content_type = part.get_content_type()

                disposition = str(
                    part.get(
                        "Content-Disposition",
                        ""
                    )
                )


                if "attachment" in disposition:

                    continue


                payload = part.get_payload(
                    decode=True
                )


                if not payload:

                    continue


                text = payload.decode(
                    "utf-8",
                    errors="ignore"
                )


                if content_type == "text/plain":

                    body_text += text


                elif content_type == "text/html":

                    body_html += text



        else:

            payload = msg.get_payload(
                decode=True
            )

            if payload:

                body_text = payload.decode(
                    "utf-8",
                    errors="ignore"
                )


        return body_text, body_html



    def extract_links(
        self,
        html
    ):

        if not html:

            return []


        return list(
            set(
                re.findall(
                    r'https?://[^\s"\']+',
                    html
                )
            )
        )



    def extract_attachments(
        self,
        msg
    ):

        attachments = []


        for part in msg.walk():

            filename = part.get_filename()

            if filename:

                attachments.append(
                    self.decode(filename)
                )


        return attachments



    def fetch_latest(
        self,
        folder="Inbox",
        limit=10
    ):

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


            status, data = mail.select(
                folder
            )


            if status != "OK":

                return []



            _, messages = mail.search(
                None,
                "ALL"
            )


            ids = messages[0].split()[-limit:]


            results = []


            for num in reversed(ids):


                _, msg_data = mail.fetch(
                    num,
                    "(RFC822)"
                )


                raw = msg_data[0][1]


                msg = message_from_bytes(
                    raw
                )


                body_text, body_html = (
                    self.extract_body(
                        msg
                    )
                )


                received_date = ""


                try:

                    received_date = (
                        parsedate_to_datetime(
                            msg.get(
                                "Date",
                                ""
                            )
                        )
                        .isoformat()
                    )

                except:

                    pass



                results.append(

                    {

                        "message_id":
                            msg.get(
                                "Message-ID",
                                ""
                            ),


                        "source":
                            "YAHOO",


                        "sender":
                            self.decode(
                                msg.get(
                                    "From"
                                )
                            ),


                        "subject":
                            self.decode(
                                msg.get(
                                    "Subject"
                                )
                            ),


                        "folder":
                            folder,


                        "received_date":
                            received_date,


                        "body_text":
                            body_text,


                        "body_html":
                            body_html,


                        "links":
                            self.extract_links(
                                body_html
                            ),


                        "attachments":
                            self.extract_attachments(
                                msg
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
