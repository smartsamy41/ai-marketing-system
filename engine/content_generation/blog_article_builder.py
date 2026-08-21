import json
from pathlib import Path
from html import escape

from engine.template_renderer import TemplateRenderer

from app.templates.base_components import (
    get_eeat_footer,
    get_cookie_consent_script
)


class BlogArticleBuilder:

    def __init__(self):

        self.renderer = TemplateRenderer()

        self.asset_graph_file = Path(
            "data_master/content_production/"
            "affiliate_asset_output/"
            "affiliate_asset_injection_graph.json"
        )


    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def clean(value):

        if value is None:
            return ""

        text = str(value).strip()

        if text.lower() in {
            "",
            "nan",
            "none",
            "null"
        }:
            return ""

        return text


    def load_json(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)


    # =========================================================
    # AFFILIATE ASSET
    # =========================================================

    def get_product_assets(
        self,
        product_id
    ):

        graph = self.load_json(
            self.asset_graph_file
        )

        return (
            graph
            .get("products", {})
            .get(product_id, [])
        )


    def select_primary_asset(
        self,
        product
    ):

        product_id = self.clean(
            product.get("product_id")
        )

        partner = self.clean(
            product.get("partner")
        ).lower()

        assets = self.get_product_assets(
            product_id
        )

        if not assets:
            return None


        priorities = {

            "check24": [
                "calculator",
                "short_calculator",
                "direct_link",
                "banner_300x250",
                "banner_728x90",
                "verified_routing_link"
            ],

            "tarifcheck": [
                "calculator",
                "direct_link",
                "short_calculator",
                "banner_300x250",
                "banner_728x90",
                "verified_routing_link"
            ],

            "amazon": [
                "verified_routing_link",
                "direct_link",
                "affiliate_asset"
            ],

            "telekom": [
                "verified_routing_link",
                "direct_link",
                "affiliate_asset"
            ]
        }


        wanted = priorities.get(
            partner,
            [
                "verified_routing_link",
                "direct_link",
                "calculator",
                "banner_300x250"
            ]
        )


        for asset_type in wanted:

            for asset in assets:

                if (
                    asset.get("asset_type")
                    == asset_type
                    and asset.get(
                        "payload_available"
                    )
                    and asset.get(
                        "source_verified"
                    )
                ):

                    return asset


        for asset in assets:

            if (
                asset.get(
                    "payload_available"
                )
                and asset.get(
                    "source_verified"
                )
            ):

                return asset


        return None


    def render_affiliate_area(
        self,
        product
    ):

        partner = self.clean(
            product.get("partner")
        ).lower()

        asset = self.select_primary_asset(
            product
        )


        if not asset:

            return """
<p>
Für dieses Thema ist derzeit kein freigegebenes
Partner-Werbemittel hinterlegt.
</p>
"""


        payload = self.clean(
            asset.get("payload")
        )

        asset_type = self.clean(
            asset.get("asset_type")
        )

        compliance = (
            asset.get(
                "compliance",
                {}
            )
            or {}
        )


        disclosure = self.clean(
            compliance.get(
                "kennzeichnung"
            )
        )


        extra = ""


        if partner == "tarifcheck":

            extra = """
<p>
<strong>
powered by TARIFCHECK24 GmbH
</strong>
</p>

<p>
Free Basics ist Tippgeber und nicht
Versicherungsvermittler.
</p>
"""


        if partner == "telekom":

            return f"""
{extra}

<p>
<strong>Werbung / Anzeige</strong>
</p>

<p>
Weitere Informationen und Angebote finden Sie
im offiziellen Telekom-Profis-Shop von Free Basics.
</p>

<a href="{escape(payload)}"
   target="_blank"
   rel="sponsored nofollow noopener">

Zum Telekom Profis Shop

</a>
"""


        if asset_type in {
            "direct_link",
            "verified_routing_link",
            "affiliate_asset"
        }:

            if partner == "amazon":

                button_text = (
                    "Bei Amazon ansehen"
                )

            elif partner == "tarifcheck":

                button_text = (
                    "Vergleich starten"
                )

            elif partner == "check24":

                button_text = (
                    "Vergleich starten"
                )

            else:

                button_text = (
                    "Weitere Informationen"
                )


            return f"""
{extra}

<p>
{escape(disclosure)}
</p>

<a href="{escape(payload)}"
   target="_blank"
   rel="sponsored nofollow noopener">

{button_text}

</a>
"""


        return f"""
{extra}

<p>
{escape(disclosure)}
</p>

<div class="official-affiliate-asset">

{payload}

</div>
"""


    # =========================================================
    # DIRECT ANSWER
    # =========================================================

    def create_direct_answer(
        self,
        product
    ):

        name = self.clean(
            product.get("name")
        )

        summary = self.clean(
            product.get("summary")
        )


        if not summary:

            return f"""
<p>
<strong>{escape(name)}</strong> ist ein Thema aus dem
Informationsangebot von Free Basics.
</p>
"""


        return f"""
<p>
<strong>{escape(name)}:</strong>
{escape(summary)}
</p>
"""


    # =========================================================
    # CONTENT
    # =========================================================

    def create_content(
        self,
        product
    ):

        content = ""


        key_facts = (
            product.get(
                "key_facts",
                []
            )
            or []
        )


        comparison_matrix = (
            product.get(
                "comparison_matrix",
                []
            )
            or []
        )


        if key_facts:

            content += """

<section>

<h2>Welche Fakten sind wichtig?</h2>

<ul>
"""

            for fact in key_facts:

                content += (
                    f"<li>{escape(str(fact))}</li>"
                )

            content += """

</ul>

</section>
"""


        if comparison_matrix:

            content += """

<section>

<h2>Welche Daten sollten verglichen werden?</h2>

<table>

<tbody>
"""

            for item in comparison_matrix:

                field = escape(
                    str(
                        item.get(
                            "field",
                            ""
                        )
                    )
                )

                value = escape(
                    str(
                        item.get(
                            "value",
                            ""
                        )
                    )
                )

                content += f"""

<tr>
<th>{field}</th>
<td>{value}</td>
</tr>
"""

            content += """

</tbody>

</table>

</section>
"""


        if not content:

            content = """

<section>

<h2>Welche Informationen sind relevant?</h2>

<p>
Dieser Artikel basiert auf den im Free-Basics-
Knowledge-Layer hinterlegten Produkt- und
Partnerinformationen.
</p>

</section>
"""


        return content


    # =========================================================
    # FAQ
    # =========================================================

    def create_faq_html(
        self,
        product
    ):

        html = ""

        faq = (
            product.get(
                "faq",
                []
            )
            or []
        )


        for item in faq:

            question = escape(
                self.clean(
                    item.get(
                        "question"
                    )
                )
            )

            answer = escape(
                self.clean(
                    item.get(
                        "answer"
                    )
                )
            )

            if not question or not answer:
                continue


            html += f"""

<div class="faq-item">

<h3>{question}</h3>

<p>{answer}</p>

</div>
"""


        return html


    def create_faq_schema(
        self,
        product,
        canonical_url
    ):

        entities = []

        faq = (
            product.get(
                "faq",
                []
            )
            or []
        )


        for item in faq:

            question = self.clean(
                item.get(
                    "question"
                )
            )

            answer = self.clean(
                item.get(
                    "answer"
                )
            )


            if not question or not answer:
                continue


            entities.append(
                {
                    "@type":
                        "Question",

                    "name":
                        question,

                    "acceptedAnswer":
                        {
                            "@type":
                                "Answer",

                            "text":
                                answer
                        }
                }
            )


        if not entities:

            return ""


        return json.dumps(
            {
                "@context":
                    "https://schema.org",

                "@type":
                    "FAQPage",

                "@id":
                    f"{canonical_url}#faq",

                "mainEntity":
                    entities
            },
            ensure_ascii=False,
            indent=2
        )


    # =========================================================
    # SOURCES
    # =========================================================

    def create_sources(
        self,
        product
    ):

        html = ""

        sources = (
            product.get(
                "sources",
                []
            )
            or []
        )


        for source in sources:

            if isinstance(
                source,
                dict
            ):

                label = self.clean(
                    source.get("name")
                    or source.get("title")
                    or source.get("source")
                    or source.get("url")
                )

                url = self.clean(
                    source.get("url")
                )


                if url:

                    html += f"""
<li>
<a href="{escape(url)}"
   target="_blank"
   rel="noopener">
{escape(label)}
</a>
</li>
"""

                elif label:

                    html += (
                        f"<li>{escape(label)}</li>"
                    )


            else:

                value = self.clean(
                    source
                )

                if value:

                    html += (
                        f"<li>{escape(value)}</li>"
                    )


        if not html:

            html = """
<li>
Produkt- und Partnerdaten aus dem
Free-Basics-Knowledge-Layer.
</li>
"""


        return html


    # =========================================================
    # RELATED CONTENT
    # =========================================================

    def create_related(
        self,
        related_products
    ):

        html = "<ul>"


        for item in (
            related_products
            or []
        ):

            if isinstance(
                item,
                dict
            ):

                product_id = self.clean(
                    item.get(
                        "product_id"
                    )
                )

                category = self.clean(
                    item.get(
                        "category"
                    )
                )


                if product_id:

                    html += f"""

<li>
<a href="/lp/{escape(product_id)}">
{escape(category or product_id)}
</a>
</li>
"""

            else:

                value = self.clean(
                    item
                )

                if value:

                    html += (
                        f"<li>{escape(value)}</li>"
                    )


        html += "</ul>"

        return html


    # =========================================================
    # INTERNAL LINKS
    # =========================================================

    def create_internal_links(
        self,
        product
    ):

        silo = self.clean(
            product.get("silo")
        )

        cluster = self.clean(
            product.get("cluster")
            or product.get("category")
        )


        links = []


        if silo:

            links.append(
                (
                    f"/{silo.replace('_', '-')}/",
                    silo.replace(
                        "_",
                        " "
                    ).title()
                )
            )


        if silo and cluster:

            cluster_slug = (
                cluster.lower()
                .replace(" ", "-")
                .replace("ä", "ae")
                .replace("ö", "oe")
                .replace("ü", "ue")
            )

            links.append(
                (
                    f"/{silo.replace('_', '-')}/{cluster_slug}/",
                    cluster
                )
            )


        html = "<ul>"


        for url, label in links:

            html += f"""

<li>
<a href="{escape(url)}">
{escape(label)}
</a>
</li>
"""


        html += "</ul>"

        return html


    # =========================================================
    # ARTICLE SCHEMA
    # =========================================================

    def create_article_schema(
        self,
        product,
        canonical_url
    ):

        name = self.clean(
            product.get("name")
        )

        summary = self.clean(
            product.get("summary")
        )

        author = self.clean(
            product.get("author")
        ) or "Redaktion Free Basics"

        updated = self.clean(
            product.get("updated_at")
        )


        schema = {

            "@context":
                "https://schema.org",

            "@type":
                "Article",

            "@id":
                f"{canonical_url}#article",

            "mainEntityOfPage":
                canonical_url,

            "headline":
                name,

            "description":
                summary,

            "author":
                {
                    "@type":
                        "Person",

                    "name":
                        author
                },

            "publisher":
                {
                    "@type":
                        "Organization",

                    "name":
                        "Free Basics",

                    "url":
                        "https://freebasics.online"
                }
        }


        if updated:

            schema[
                "dateModified"
            ] = updated


        return json.dumps(
            schema,
            ensure_ascii=False,
            indent=2
        )


    # =========================================================
    # BUILD
    # =========================================================

    def build(
        self,
        product,
        facts=None,
        related_products=None
    ):

        facts = facts or {}

        related_products = (
            related_products
            or product.get(
                "related_products",
                []
            )
            or []
        )


        name = self.clean(
            product.get("name")
        )


        description = self.clean(
            product.get("summary")
        )


        canonical_url = self.clean(
            product.get("article_url")
        )


        if not canonical_url:

            product_id = self.clean(
                product.get(
                    "product_id"
                )
            )

            canonical_url = (
                "https://freebasics.online/"
                f"blog/{product_id.lower()}-ratgeber"
            )


        faq_html = self.create_faq_html(
            product
        )


        article = {

            "title":
                name,

            "description":
                description,

            "ai_summary":
                description,

            "direct_answer":
                self.create_direct_answer(
                    product
                ),

            "content":
                self.create_content(
                    product
                ),

            "entity_context":
                f"""
<p>
<strong>Silo:</strong>
{escape(self.clean(product.get('silo')))}
</p>

<p>
<strong>Cluster:</strong>
{escape(self.clean(product.get('cluster')))}
</p>

<p>
Die Inhalte basieren auf dem
Free-Basics-Knowledge-Layer und den
hinterlegten Produkt- und Partnerdaten.
</p>
""",

            "sources":
                self.create_sources(
                    product
                ),

            "questions":
                faq_html,

            "faq":
                faq_html,

            "related_products":
                self.create_related(
                    related_products
                ),

            "internal_links":
                self.create_internal_links(
                    product
                ),

            "affiliate_area":
                self.render_affiliate_area(
                    product
                ),

            "newsletter":
                f"""
<p>
Neue Ratgeber und Informationen
zum Themenbereich
<strong>
{escape(self.clean(product.get('newsletter_segment')))}
</strong>
erhalten.
</p>

<a href="/newsletter">
Newsletter Anmeldung
</a>
""",

            "footer":
                get_eeat_footer(),

            "cookie_consent":
                get_cookie_consent_script(),

            "article_schema":
                self.create_article_schema(
                    product,
                    canonical_url
                ),

            "faq_schema":
                self.create_faq_schema(
                    product,
                    canonical_url
                ),

            "canonical_url":
                canonical_url,

            "og_image_url":
                self.clean(
                    product.get(
                        "og_image_url"
                    )
                    or product.get(
                        "image_url"
                    )
                ),

            "author":
                self.clean(
                    product.get(
                        "author"
                    )
                )
                or "Redaktion Free Basics",

            "reviewed_by":
                self.clean(
                    product.get(
                        "reviewed_by"
                    )
                ),

            "updated_at":
                self.clean(
                    product.get(
                        "updated_at"
                    )
                ),

            "silo":
                self.clean(
                    product.get(
                        "silo"
                    )
                ),

            "cluster":
                self.clean(
                    product.get(
                        "cluster"
                    )
                ),

            "newsletter_segment":
                self.clean(
                    product.get(
                        "newsletter_segment"
                    )
                ),

            "facts":
                facts
        }


        return article


    # =========================================================
    # RENDER
    # =========================================================

    def render(
        self,
        article
    ):

        return self.renderer.render(

            "blog/geo_authority_article.html",

            article

        )


if __name__ == "__main__":

    builder = BlogArticleBuilder()

    print(
        "BlogArticleBuilder READY"
    )
