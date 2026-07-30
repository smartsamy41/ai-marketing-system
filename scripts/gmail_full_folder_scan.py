from engine.gmail_reader import GmailReader


reader = GmailReader()

mail = reader.connect()

status, folders = mail.list()

print("GMAIL ORDNER")
print("================")

for folder in folders:
    print(folder.decode())

mail.logout()
