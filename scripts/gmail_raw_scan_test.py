from engine.gmail_reader import GmailReader

reader = GmailReader()

mails = reader.fetch_latest(20)

print("ANZAHL:", len(mails))

for mail in mails:
    print("----------------")
    print("SENDER:", mail.get("sender"))
    print("SUBJECT:", mail.get("subject"))
