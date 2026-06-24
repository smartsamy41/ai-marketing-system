import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


# =========================
# EMAIL SENDER ENGINE (PRODUCTION)
# =========================
class EmailSenderEngine:

    def __init__(self, smtp_host, smtp_port, email, password):

        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    # =========================
    # SEND SINGLE EMAIL
    # =========================
    def send_email(self, to_email, subject, html_content):

        try:

            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(html_content, "html"))

            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)

            server.send_message(msg)
            server.quit()

            return {
                "status": "SENT",
                "to": to_email,
                "subject": subject,
                "timestamp": str(datetime.utcnow())
            }

        except Exception as e:

            return {
                "status": "ERROR",
                "message": str(e)
            }

    # =========================
    # SEND CAMPAIGN (AUTOPILOT)
    # =========================
    def send_campaign(self, emails):

        results = []

        for mail in emails:

            results.append(
                self.send_email(
                    mail["to"],
                    mail["subject"],
                    mail["html"]
                )
            )

        return {
            "status": "CAMPAIGN_SENT",
            "count": len(results),
            "results": results
        }
