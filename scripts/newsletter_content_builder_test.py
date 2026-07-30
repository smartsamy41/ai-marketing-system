from engine.newsletter_content_builder import NewsletterContentBuilder


builder = NewsletterContentBuilder()


campaign = {
    "partner": "Check24",
    "product_id": "CHK24_001",
    "category": "Strom"
}


product = {
    "landingpage_url":
        "https://freebasics.online/lp/CHK24_001"
}


result = builder.build(
    campaign,
    product
)


print(result["status"])
print(result["subject"])
print(result["html"][:500])
