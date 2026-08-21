import json
from pathlib import Path
from datetime import datetime, timezone


class HTMLPageGenerator:

    def __init__(self):

        self.architecture_file = Path(
            "data_master/content_production/rendered_page_architecture.json"
        )

        self.product_file = Path(
            "data_master/catalog/product_master_44.json"
        )

        self.knowledge_file = Path(
            "data_master/knowledge_master/product_knowledge_master.json"
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



    def safe_text(self, value):

        if value is None:
            return ""

        if isinstance(value, list):

            return "<br>".join(
                str(x)
                for x in value
            )

        if isinstance(value, dict):

            return "<br>".join(
                f"{k}: {v}"
                for k, v in value.items()
            )

        return str(value)



    def create_facts(self, facts):

        if not facts:
            return "<p>Keine weiteren geprüften Fakten verfügbar.</p>"


        html = "<ul>"

        if isinstance(facts, list):

            for item in facts:

                html += f"""
<li>
{self.safe_text(item)}
</li>
"""

        elif isinstance(facts, dict):

            for key,value in facts.items():

                html += f"""
<li>
<strong>{key}</strong>: {self.safe_text(value)}
</li>
"""


        html += "</ul>"

        return html



    def create_faq(self, faq):

        if not faq:
            return "<p>Keine FAQ-Daten verfügbar.</p>"


        html = ""


        if isinstance(faq,list):

            for item in faq:

                if isinstance(item,dict):

                    question = item.get(
                        "question",
                        "Frage"
                    )

                    answer = item.get(
                        "answer",
                        ""
                    )

                else:

                    question = "Frage"
                    answer = item


                html += f"""
<div class="faq-item">

<h3>
{question}
</h3>

<p>
{self.safe_text(answer)}
</p>

</div>
"""


        return html



    def create_html(
        self,
        page,
        product,
        knowledge
    ):


        product_id = product.get(
            "product_id",
            "UNKNOWN"
        )


        name = product.get(
            "name",
            product_id
        )


        summary = product.get(
            "summary",
            ""
        )


        category = product.get(
            "category",
            ""
        )


        facts = product.get(
            "key_facts",
            []
        )


        faq = product.get(
            "faq",
            []
        )


        sources = product.get(
            "sources",
            []
        )


        links = product.get(
            "internal_links",
            []
        )


        updated = product.get(
            "updated_at",
            ""
        )



        knowledge_context = ""

        if knowledge:

            knowledge_context = self.safe_text(
                knowledge.get(
                    "knowledge",
                    {}
                ).get(
                    "llm_context",
                    ""
                )
            )



        html = f"""<!DOCTYPE html>
<html lang="de">

<head>

<meta charset="UTF-8">

<title>
{name} | Free Basics
</title>


<meta name="description" content="{summary}">


<link rel="canonical" href="/produkte/{product_id}">


<meta property="og:title" content="{name} | Free Basics">

<meta property="og:description" content="{summary}">


</head>


<body>


<header>

<h1>
{name}
</h1>

<p>
Kategorie: {category}
</p>

</header>



<main>



<section>

<h2>
Kurzantwort
</h2>

<p>
{summary}
</p>

</section>



<section>

<h2>
Ratgeber
</h2>


<p>
{knowledge_context}
</p>


</section>



<section>

<h2>
Wichtige Fakten
</h2>


{self.create_facts(facts)}


</section>



<section>

<h2>
Vergleich und Informationen
</h2>


<p>
Weitere geprüfte Informationen werden aus den hinterlegten Quellen erstellt.
</p>


</section>



<section>

<h2>
Häufige Fragen
</h2>


{self.create_faq(faq)}


</section>



<section>

<h2>
Quellen
</h2>

{self.create_facts(sources)}

</section>



<section>

<h2>
Weitere Informationen
</h2>

{self.create_facts(links)}

</section>



<section class="affiliate-box">

<h2>
Werbung / Anzeige
</h2>


<p>
Dieses Angebot enthält Partnerlinks und Werbemittel.
</p>


</section>



<footer>

<p>
Free Basics
</p>

<p>
Aktualisiert: {updated}
</p>


</footer>


</main>


</body>

</html>
"""


        return html



    def build(self):


        architecture = self.load_json(
            self.architecture_file
        )


        products_data = self.load_json(
            self.product_file
        )


        knowledge_data = self.load_json(
            self.knowledge_file
        )


        products = {

            p["product_id"]: p

            for p in products_data.get(
                "products",
                []
            )

        }


        knowledge = {

            p["product_id"]: p

            for p in knowledge_data.get(
                "products",
                []
            )

        }



        self.output.mkdir(
            parents=True,
            exist_ok=True
        )



        created = 0



        for page in architecture.get(
            "pages",
            []
        ):


            product_id = page.get(
                "product_id"
            )


            if not product_id:
                continue



            product = products.get(
                product_id,
                {}
            )


            knowledge_item = knowledge.get(
                product_id,
                {}
            )



            html = self.create_html(
                page,
                product,
                knowledge_item
            )



            file = self.output / (
                f"{product_id}.html"
            )



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
            datetime.now(
                timezone.utc
            ).isoformat()
        )



if __name__ == "__main__":

    HTMLPageGenerator().build()
