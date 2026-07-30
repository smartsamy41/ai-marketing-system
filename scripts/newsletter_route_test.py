from engine.newsletter_mail_router import NewsletterMailRouter

router = NewsletterMailRouter()

tests = [

{
"sender":"Amazon Ads <noreply@ads.amazon.com>",
"subject":"Stellen Sie Ihre Bücher potenziellen neuen Lesern vor"
},

{
"sender":"CHECK24-Partnerprogramm <jan.schust@check24-partnerprogramm.de>",
"subject":"C24 Bank: 50 € Provision für jeden Sale sichern"
},

{
"sender":"Tarifcheck.de-Partnerprogramm <winkler.clemens@tarifcheck-partnerprogramm.de>",
"subject":"50 € pro Sale: Rechtsschutzversicherung"
},

{
"sender":"Telekom Profis News <support@telekom-profis.de>",
"subject":"MagentaMobil Aktion"
},

{
"sender":"Telekom Deutschland GmbH <rechnungonline@telekom.de>",
"subject":"Ihre Telekom Rechnung Juli 2026"
}

]


for mail in tests:

    result = router.route(mail)

    print("----------------")
    print(mail["sender"])
    print(result)
