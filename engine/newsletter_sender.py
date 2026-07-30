import smtplib
from email.message import EmailMessage

from engine.secret_manager import SecretManager


class NewsletterSender:

    def __init__(self):

        secrets = SecretManager()

        self.email = secrets.get(
            "GMAIL_ACCOUNT_EMAIL"
        )

        self.password = secrets.get(
            "GMAIL_APP_PASSWORD"
        )

        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 465


    def send_doi_mail(
        self,
        recipient,
        token
    ):

        confirm_url = (
            "https://freebasics.online/newsletter/confirm?token="
            + token
        )

        msg = EmailMessage()

        msg["Subject"] = (
            "Free Basics Newsletter bestätigen"
        )

        msg["From"] = self.email

        msg["To"] = recipient


        msg.set_content(
            f"""
Hallo,

vielen Dank für deine Anmeldung zum Free Basics Newsletter.

Bitte bestätige deine E-Mail-Adresse über diesen Link:

{confirm_url}

Falls du dich nicht angemeldet hast, kannst du diese Nachricht ignorieren.

Viele Grüße

Free Basics
"""
        )


        with smtplib.SMTP_SSL(
            self.smtp_host,
            self.smtp_port
        ) as server:

            server.login(
                self.email,
                self.password
            )

            server.send_message(
                msg
            )


        return True
