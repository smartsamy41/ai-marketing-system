import json
from pathlib import Path
from datetime import datetime, timezone


class HTMLPageGenerator:

    def __init__(self):

        self.source = Path(
            "data_master/content_production/rendered_page_architecture.json"
        )

        self.output = Path(
            "data_master/content_production/generated_pages"
        )


    def load_json(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)


    def create_html(self, page):

        product_id = page.get(
            "product_id",
            "UNKNOWN"
        )

        html = f"""<!DOCTYPE html>
<html lang="de">

<head>

<meta charset="UTF-8">

<title>
Free Basics - {product_id}
</title>

</head>


<body>


<header>

<h1>
Free Basics
</h1>

</header>



<main>


<section aria-label="Produkt">

<h2>
{product_id}
</h2>


</section>



<section aria-label="Kurzantwort">

<h2>
Kurzantwort
</h2>

<p>
Informationen werden aus geprüften Quellen erstellt.
</p>

</section>



<section aria-label="Artikel">

<h2>
Artikel
</h2>

<p>
CONTENT_PLACEHOLDER
</p>

</section>



<section aria-label="Fragen">

<h2>
Häufige Fragen
</h2>


<div>

FAQ_PLACEHOLDER

</div>


</section>



<section aria-label="Verwandte Inhalte">

<h2>
Weitere Informationen
</h2>


</section>



<section aria-label="Hinweise">

<h2>
Hinweise
</h2>


<p>
Affiliate Offenlegung und rechtliche Informationen.
</p>


</section>


</main>



<footer>

Free Basics

</footer>


</body>

</html>
"""

        return html



    def build(self):

        data = self.load_json(
            self.source
        )


        pages = data.get(
            "pages",
            []
        )


        self.output.mkdir(
            parents=True,
            exist_ok=True
        )


        created = 0


        for page in pages:

            product_id = page.get(
                "product_id"
            )


            if not product_id:
                continue


            html = self.create_html(
                page
            )


            file = self.output / f"{product_id}.html"


            with open(
                file,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(html)


            created += 1



        print(
            "HTML PAGES GENERATED"
        )


        print(
            "PAGES:",
            created
        )


        print(
            "TIME:",
            datetime.now(timezone.utc).isoformat()
        )



if __name__ == "__main__":

    HTMLPageGenerator().build()
