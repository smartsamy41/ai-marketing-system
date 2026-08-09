import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import subprocess
import re


class GmailReader:


    def __init__(self):

        self.email = self.secret(
            "GMAIL_ACCOUNT_EMAIL"
        )

        self.password = self.secret(
            "GMAIL_APP_PASSWORD"
        )


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
            "imap.gmail.com",
            993
        )

        mail.login(
            self.email,
            self.password
        )

        return mail



    def decode_text(self, value):

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



    def extract_body(self, msg):

        text = ""
        html = ""

        if msg.is_multipart():

            for part in msg.walk():

                ctype = part.get_content_type()

                if ctype not in [
                    "text/plain",
                    "text/html"
                ]:
                    continue

                payload = part.get_payload(
                    decode=True
                )

                if not payload:
                    continue

                content = payload.decode(
                    "utf-8",
                    errors="ignore"
                )

                if ctype == "text/plain":
                    text += content

                if ctype == "text/html":
                    html += content


        else:

            payload = msg.get_payload(
                decode=True
            )

            if payload:

                text = payload.decode(
                    "utf-8",
                    errors="ignore"
                )


        return (
            text[:20000],
            html[:20000]
        )



    def extract_links(self, html):

        if not html:
            return []

        return list(
            set(
                re.findall(
                    r"https?://[^\s\"']+",
                    html
                )
            )
        )



    def fetch_latest(self, limit=20):

        mail = self.connect()

        results = []


        try:

            status, _ = mail.select(
                "INBOX"
            )

            if status != "OK":
                return []


            _, data = mail.search(
                None,
                "ALL"
            )


            ids = data[0].split()[-limit:]


            for num in reversed(ids):

                # nur Header laden
                _, header = mail.fetch(
                    num,
                    "(BODY.PEEK[HEADER])"
                )


                raw = header[0][1]


                msg = email.message_from_bytes(
                    raw
                )


                results.append(

                    {
                        "message_id":
                            msg.get(
                                "Message-ID",
                                ""
                            ),

                        "sender":
                            self.decode_text(
                                msg.get(
                                    "From",
                                    ""
                                )
                            ),

                        "subject":
                            self.decode_text(
                                msg.get(
                                    "Subject",
                                    ""
                                )
                            ),

                        "received_date":
                            msg.get(
                                "Date",
                                ""
                            ),

                        "body_text":"",
                        "body_html":"",
                        "links":[],
                        "attachments":[]

                    }

                )


            return results


        finally:

            mail.logout()



    def fetch_from_folder(
        self,
        folder,
        limit=10
    ):

        mail = self.connect()

        results=[]

        try:

            status,_ = mail.select(
                f'"{folder}"'
            )

            if status != "OK":
                return []


            _, data = mail.search(
                None,
                "ALL"
            )


            ids = data[0].split()[-limit:]


            for num in reversed(ids):

                _, header = mail.fetch(
                    num,
                    "(BODY.PEEK[HEADER])"
                )


                msg = email.message_from_bytes(
                    header[0][1]
                )


                results.append(

                    {
                        "message_id":
                            msg.get(
                                "Message-ID",
                                ""
                            ),

                        "sender":
                            self.decode_text(
                                msg.get(
                                    "From",
                                    ""
                                )
                            ),

                        "subject":
                            self.decode_text(
                                msg.get(
                                    "Subject",
                                    ""
                                )
                            ),

                        "received_date":
                            msg.get(
                                "Date",
                                ""
                            ),

                        "body_text":"",
                        "body_html":"",
                        "links":[],
                        "attachments":[]
                    }
                )


            return results


        finally:

            mail.logout()
