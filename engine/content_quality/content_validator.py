class ContentValidator:


    def validate_landingpage(self, page):

        required = [
            "product_id",
            "title",
            "partner",
            "tracking_url"
        ]

        missing = [
            x for x in required
            if not page.get(x)
        ]

        return {
            "type":"landingpage",
            "valid": len(missing)==0,
            "missing": missing
        }



    def validate_article(self, article):

        required = [
            "title",
            "author",
            "reviewer",
            "published_at",
            "sources"
        ]

        missing = [
            x for x in required
            if not article.get(x)
        ]

        return {
            "type":"article",
            "valid": len(missing)==0,
            "missing": missing
        }



if __name__ == "__main__":

    validator = ContentValidator()

    print(
        validator.validate_landingpage(
            {
                "product_id":"CHK24_001",
                "title":"Strom",
                "partner":"check24",
                "tracking_url":"test"
            }
        )
    )
