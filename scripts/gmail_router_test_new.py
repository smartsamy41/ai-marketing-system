from engine.gmail_newsletter_router import GmailNewsletterRouter

router = GmailNewsletterRouter()

tests = [

{
"sender":"Amazon Ads <noreply@ads.amazon.com>",
"subject":"Stellen Sie Ihre Bücher potenziellen neuen Lesern vor"
},

{
"sender":"Amazon Associates <associates@amazon.de>",
"subject":"PartnerNet Update"
},

{
"sender":"CHECK24-Partnerprogramm <jan.schust@check24-partnerprogramm.de>",
"subject":"C24 Bank Provision"
},

{
"sender":"Tarifcheck.de-Partnerprogramm <winkler.clemens@tarifcheck-partnerprogramm.de>",
"subject":"Rechtsschutzversicherung Aktion"
}

]


for mail in tests:
    print("----------------")
    print(mail["sender"])
    print(router.route(mail))
