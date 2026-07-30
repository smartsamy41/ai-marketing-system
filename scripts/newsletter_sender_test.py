from engine.newsletter_sender import NewsletterSender

sender = NewsletterSender()

result = sender.send_doi_mail(
    "samyjendoubi@gmail.com",
    "TEST_TOKEN_12345"
)

print("SEND RESULT:", result)
