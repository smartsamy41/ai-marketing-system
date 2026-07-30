from engine.gmail_reader import GmailReader

print("START Gmail Test")

reader = GmailReader()

print("Reader erstellt")

mails = reader.fetch_latest(10)

print("ANZAHL:", len(mails))

for mail in mails:
    print("----------------")
    print("FROM:", mail.get("sender"))
    print("SUBJECT:", mail.get("subject"))

print("FERTIG")
