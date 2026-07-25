class URLResolver:

    def __init__(
        self,
        domain="https://freebasics.online"
    ):
        self.domain = domain


    def create_slug(self, product):

        name = product.get("name", "")

        slug = (
            name.lower()
            .replace("ä","ae")
            .replace("ö","oe")
            .replace("ü","ue")
            .replace(" ","-")
        )

        return slug


    def landingpage_url(self, product):

        slug = self.create_slug(product)

        return f"{self.domain}/angebote/{slug}"


    def article_url(self, product):

        slug = self.create_slug(product)

        return f"{self.domain}/blog/{slug}-ratgeber"


if __name__ == "__main__":

    resolver = URLResolver()

    product = {
        "name":"Strom"
    }

    print(resolver.landingpage_url(product))
    print(resolver.article_url(product))
