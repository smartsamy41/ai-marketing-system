import json
from pathlib import Path
from html import escape

from engine.publishing.repository_publisher import RepositoryPublisher


class GeoPageRenderer:

    def __init__(self):

        self.nodes_file = Path(
            "data_master/geo_layer/geo_content_nodes.json"
        )

        self.publisher = RepositoryPublisher()


    def load_json(self, path):

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)


    def find_node(
        self,
        product_id,
        location_id
    ):

        data = self.load_json(
            self.nodes_file
        )

        for node in data.get(
            "nodes",
            []
        ):

            if (
                node.get("product_id") == product_id
                and
                node.get("location_id") == location_id
            ):

                return node

        return {}


    def render(
        self,
        node
    ):

        title = (
            f"{node.get('product_name')} in "
            f"{node.get('location_name')}"
        )

        canonical = node.get(
            "canonical_url",
            ""
        )

        direct_answer = escape(
            node.get(
                "direct_answer",
                ""
            )
        )

        facts = node.get(
            "verified_facts",
            []
        )

        source_urls = node.get(
            "source_urls",
            []
        )

        fact_html = "\n".join(
            f"<li>{escape(str(x))}</li>"
            for x in facts
        )

        source_html = "\n".join(
            f'''
<li>
<a href="{escape(str(url))}"
   target="_blank"
   rel="noopener">
{escape(str(url))}
</a>
</li>
'''
            for url in source_urls
        )


        schema = {

            "@context":
                "https://schema.org",

            "@graph": [

                {
                    "@type":
                        "WebPage",

                    "@id":
                        canonical,

                    "url":
                        canonical,

                    "name":
                        title,

                    "about":
                        {
                            "@type":
                                "Place",

                            "name":
                                node.get(
                                    "location_name"
                                ),

                            "sameAs":
                                (
                                    "https://www.wikidata.org/wiki/"
                                    f"{node.get('wikidata_id')}"
                                )
                        }
                },

                {
                    "@type":
                        "BreadcrumbList",

                    "itemListElement": [

                        {
                            "@type":
                                "ListItem",
                            "position":
                                1,
                            "name":
                                "Home",
                            "item":
                                "https://freebasics.online/"
                        },

                        {
                            "@type":
                                "ListItem",
                            "position":
                                2,
                            "name":
                                node.get(
                                    "silo",
                                    ""
                                ),
                            "item":
                                (
                                    "https://freebasics.online/"
                                    f"{node.get('silo')}/"
                                )
                        },

                        {
                            "@type":
                                "ListItem",
                            "position":
                                3,
                            "name":
                                node.get(
                                    "category",
                                    ""
                                ),
                            "item":
                                (
                                    "https://freebasics.online/"
                                    f"{node.get('silo')}/"
                                    f"{node.get('category')}/"
                                )
                        },

                        {
                            "@type":
                                "ListItem",
                            "position":
                                4,
                            "name":
                                node.get(
                                    "location_name",
                                    ""
                                ),
                            "item":
                                canonical
                        }

                    ]
                }

            ]
        }


        schema_json = json.dumps(
            schema,
            ensure_ascii=False,
            indent=2
        )


        html = f"""<!DOCTYPE html>
<html lang="de">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>{escape(title)} | Free Basics</title>

<meta name="description"
      content="{escape(node.get('direct_answer',''))}">

<link rel="canonical"
      href="{escape(canonical)}">

<meta name="robots"
      content="index, follow">

<meta property="og:type"
      content="article">

<meta property="og:site_name"
      content="Free Basics">

<meta property="og:title"
      content="{escape(title)}">

<meta property="og:description"
      content="{escape(node.get('direct_answer',''))}">

<meta property="og:url"
      content="{escape(canonical)}">

<meta name="twitter:card"
      content="summary">

<meta name="twitter:title"
      content="{escape(title)}">

<meta name="twitter:description"
      content="{escape(node.get('direct_answer',''))}">

<script type="application/ld+json">
{schema_json}
</script>

<style>

body {{
    font-family: Arial, sans-serif;
    max-width: 1000px;
    margin: auto;
    padding: 20px;
    line-height: 1.7;
    color: #222;
}}

.box {{
    border: 1px solid #ddd;
    border-radius: 14px;
    padding: 24px;
    margin: 24px 0;
}}

.hero {{
    background: #f5f7fb;
}}

.answer {{
    background: #f8fafc;
}}

a {{
    color: #0055ff;
}}

</style>

</head>

<body>

<nav class="box">
<a href="/">Home</a>
&gt;
<a href="/{escape(node.get('silo',''))}/">
{escape(node.get('silo','').title())}
</a>
&gt;
<a href="/{escape(node.get('silo',''))}/{escape(node.get('category',''))}/">
{escape(node.get('category','').title())}
</a>
&gt;
<span>{escape(node.get('location_name',''))}</span>
</nav>

<header class="box hero">

<h1>
{escape(title)}
</h1>

<p>
Stand: {escape(node.get('updated_at',''))}
</p>

</header>

<main>

<section class="box answer">

<h2>
Welche lokalen Informationen liegen für {escape(node.get('location_name',''))} vor?
</h2>

<p>
{direct_answer}
</p>

</section>

<section class="box">

<h2>
Lokale Fakten
</h2>

<ul>
{fact_html}
</ul>

</section>

<section class="box">

<h2>
Ort und Datenbasis
</h2>

<ul>
<li>
Ort:
{escape(node.get('location_name',''))}
</li>

<li>
PLZ:
{escape(node.get('postal_code',''))}
</li>

<li>
Bundesland:
{escape(node.get('state',''))}
</li>

<li>
Wikidata:
<a href="https://www.wikidata.org/wiki/{escape(node.get('wikidata_id',''))}"
   target="_blank"
   rel="noopener">
{escape(node.get('wikidata_id',''))}
</a>
</li>

<li>
Produkt-ID:
{escape(node.get('product_id',''))}
</li>

</ul>

</section>

<section class="box">

<h2>
Quellen
</h2>

<ul>
{source_html}
</ul>

</section>

<section class="box">

<h2>
Werbung / Anzeige
</h2>

<p>
Weitere Tarifinformationen können über den
zugeordneten Partnervergleich geprüft werden.
</p>

<a href="/angebote/strom"
   rel="sponsored nofollow">
Vergleich starten
</a>

</section>

</main>

<footer class="box">

<p>
Free Basics
</p>

<p>
<a href="/methodik">Methodik</a>
|
<a href="/redaktion">Redaktion</a>
|
<a href="/affiliate-hinweis">Affiliate-Hinweis</a>
|
<a href="/impressum">Impressum</a>
|
<a href="/datenschutz">Datenschutz</a>
</p>

</footer>

</body>

</html>
"""

        return html


    def publish(
        self,
        product_id,
        location_id
    ):

        node = self.find_node(
            product_id,
            location_id
        )

        if not node:

            return {
                "status":
                    "BLOCKED",

                "reason":
                    "NODE_NOT_FOUND"
            }


        html = self.render(
            node
        )


        return self.publisher.publish_geo_node(
            node,
            html
        )


if __name__ == "__main__":

    renderer = GeoPageRenderer()

    result = renderer.publish(
        "CHK24_001",
        "DE-SH-LUEBECK-Q2843"
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )
