import json
from pathlib import Path
from datetime import datetime, timezone
from html import escape

from engine.rendering.production_renderer import ProductionRenderer
from engine.self_learning_agent.internal_linking_optimizer import InternalLinkingOptimizer

from app.templates.base_components import (
    get_eeat_footer,
    get_cookie_consent_script
)


class LandingPageBuilder:

    def __init__(
        self,
        system="FREE BASICS AI MARKETING SYSTEM"
    ):

        self.system = system

        self.renderer = ProductionRenderer()

        self.link_optimizer = InternalLinkingOptimizer()

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


    def _slugify(self, text):

        return (
            self.clean(text)
            .lower()
            .replace(" ", "-")
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
        )


    def load_json(self, path):

        if not path.exists():
            return {}

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)


    # =========================================================
    # AFFILIATE ASSETS
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
                    asset.get("asset_type") == asset_type
                    and asset.get("payload_available")
                    and asset.get("source_verified")
                ):

                    return asset


        for asset in assets:

            if (
                asset.get("payload_available")
                and asset.get("source_verified")
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
Für dieses Produkt ist derzeit kein freigegebenes
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
            asset.get("compliance", {})
            or {}
        )

        disclosure = self.clean(
            compliance.get("kennzeichnung")
        )


        if partner == "telekom":

            return f"""
<p>
<strong>Werbung / Anzeige</strong>
</p>

<p>
Weitere Informationen und Angebote finden Sie
im offiziellen Telekom-Profis-Shop von Free Basics.
</p>

<a class="button"
   href="{escape(payload)}"
   target="_blank"
   rel="sponsored nofollow noopener">

Zum Telekom Profis Shop

</a>
"""


        partner_notice = ""


        if partner == "tarifcheck":

            partner_notice = """
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


        if asset_type in {
            "direct_link",
            "verified_routing_link",
            "affiliate_asset"
        }:

            if partner == "amazon":

                label = "Bei Amazon ansehen"

            elif partner in {
                "check24",
                "tarifcheck"
            }:

                label = "Vergleich starten"

            else:

                label = "Weitere Informationen"


            return f"""
{partner_notice}

<p>
{escape(disclosure)}
</p>

<a class="button"
   href="{escape(payload)}"
   target="_blank"
   rel="sponsored nofollow noopener">

{label}

</a>
"""


        return f"""
{partner_notice}

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

    def build_direct_answer(
        self,
        product
    ):

        name = self.clean(
            product.get("name")
            or product.get("product_name")
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
    # MAIN CONTENT
    # =========================================================

    def build_content(
        self,
        product
    ):

        html = []


        summary = self.clean(
            product.get("summary")
        )


        if summary:

            html.append(
                f"""
<section>

<h2>Worum geht es bei {escape(self.clean(product.get("name"))) }?</h2>

<p>
{escape(summary)}
</p>

</section>
"""
            )


        key_facts = (
            product.get(
                "key_facts",
                []
            )
            or []
        )


        if key_facts:

            html.append(
                """
<section>

<h2>Welche Fakten sind wichtig?</h2>

<ul>
"""
            )

            for fact in key_facts:

                html.append(
                    f"<li>{escape(str(fact))}</li>"
                )

            html.append(
                """
</ul>

</section>
"""
            )


        comparison = (
            product.get(
                "comparison_matrix",
                []
            )
            or []
        )


        if comparison:

            html.append(
                """
<section>

<h2>Welche Daten sollten verglichen werden?</h2>

<table>

<tbody>
"""
            )


            for item in comparison:

                field = escape(
                    self.clean(
                        item.get("field")
                    )
                )

                value = escape(
                    self.clean(
                        item.get("value")
                    )
                )


                html.append(
                    f"""
<tr>
<th>{field}</th>
<td>{value}</td>
</tr>
"""
                )


            html.append(
                """
</tbody>

</table>

</section>
"""
            )


        content = self.clean(
            product.get("content")
        )


        if content:

            html.append(
                f"""
<section>

<h2>Weitere Informationen</h2>

<p>
{escape(content)}
</p>

</section>
"""
            )


        if not html:

            html.append(
                """
<section>

<h2>Welche Informationen liegen vor?</h2>

<p>
Diese Seite basiert auf geprüften Produkt-
und Partnerinformationen aus dem
Free-Basics-Knowledge-Layer.
</p>

</section>
"""
            )


        return "\n".join(html)


    # =========================================================
    # RELATED PRODUCTS
    # =========================================================

    def build_related_products(
        self,
        products
    ):

        html = []


        for item in (
            products
            or []
        )[:8]:

            if not isinstance(
                item,
                dict
            ):
                continue


            product_id = self.clean(
                item.get("product_id")
            )

            name = self.clean(
                item.get("category")
                or item.get("name")
                or product_id
            )


            if not product_id:
                continue


            html.append(
                f"""
<div class="related-product">

<a href="/lp/{escape(product_id)}">

{escape(name)}

</a>

</div>
"""
            )


        return "\n".join(html)


    # =========================================================
    # INTERNAL LINKS
    # =========================================================

    def build_internal_links(
        self,
        product,
        related_products
    ):

        name = self.clean(
            product.get("name")
        )

        category = self.clean(
            product.get("category")
        )

        slug = self._slugify(
            name
        )


        result = self.link_optimizer.suggest_links(

            {
                "slug": slug,
                "category": category
            },

            related_products or []

        )


        html = []


        silo = self.clean(
            product.get("silo")
        )


        cluster = self.clean(
            product.get("cluster")
            or category
        )


        if silo:

            silo_slug = (
                silo.replace(
                    "_",
                    "-"
                )
            )

            html.append(
                f"""
<li>
<a href="/{escape(silo_slug)}/">
{escape(silo.replace("_", " ").title())}
</a>
</li>
"""
            )


        if silo and cluster:

            silo_slug = silo.replace(
                "_",
                "-"
            )

            cluster_slug = self._slugify(
                cluster
            )

            html.append(
                f"""
<li>
<a href="/{escape(silo_slug)}/{escape(cluster_slug)}/">
{escape(cluster)}
</a>
</li>
"""
            )


        for link in result.get(
            "links",
            []
        ):

            target = self.clean(
                link.get("to")
            )

            reason = self.clean(
                link.get("reason")
            )


            if not target:
                continue


            html.append(
                f"""
<li>
<a href="/blog/{escape(target)}-ratgeber">
{escape(reason or target)}
</a>
</li>
"""
            )


        return (
            "<ul>"
            +
            "\n".join(html)
            +
            "</ul>"
        )


    # =========================================================
    # BUILD
    # =========================================================

    def build(
        self,
        product,
        related_products=None,
        facts=None
    ):

        now = datetime.now(
            timezone.utc
        ).strftime(
            "%Y-%m-%d"
        )


        related_products = (
            related_products
            or product.get(
                "related_products",
                []
            )
            or []
        )


        product_id = self.clean(
            product.get("product_id")
        )


        name = self.clean(
            product.get("name")
            or product.get("product_name")
            or "Produkt"
        )


        category = self.clean(
            product.get("category")
        )


        partner = self.clean(
            product.get("partner")
        ).lower()


        silo = self.clean(
            product.get("silo")
        )


        cluster = self.clean(
            product.get("cluster")
            or category
        )


        newsletter_segment = self.clean(
            product.get(
                "newsletter_segment"
            )
            or silo
            or category
        )


        slug = self._slugify(
            name
        )


        canonical_url = self.clean(
            product.get(
                "landingpage_url"
            )
        )


        if not canonical_url:

            canonical_url = (
                "https://freebasics.online/"
                f"angebote/{slug}"
            )


        #
        # GEO QUALITY SHIELD PREPARATION
        #
        # Noch KEINE erfundenen lokalen Daten.
        #
        geo_verified = bool(
            product.get(
                "geo_verified",
                False
            )
        )


        page_type = self.clean(
            product.get(
                "page_type"
            )
        )


        if page_type == "geo" and not geo_verified:

            robots_meta = (
                "noindex, follow"
            )

        else:

            robots_meta = (
                "index, follow"
            )


        return {

            "system":
                self.system,

            "product_id":
                product_id,

            "title":
                name,

            "category":
                category,

            "partner":
                partner,

            "silo":
                silo,

            "cluster":
                cluster,

            "newsletter_segment":
                newsletter_segment,

            "description":
                self.clean(
                    product.get(
                        "summary"
                    )
                ),

            "direct_answer":
                self.build_direct_answer(
                    product
                ),

            "content":
                self.build_content(
                    product
                ),

            "faq":
                product.get(
                    "faq",
                    []
                )
                or [],

            "questions":
                product.get(
                    "questions",
                    []
                )
                or [],

            "sources":
                product.get(
                    "sources",
                    []
                )
                or [],

            "facts":
                facts or {},

            "affiliate_area":
                self.render_affiliate_area(
                    product
                ),

            "tracking_url":
                self.clean(
                    product.get(
                        "tracking_url"
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
                )
                or now,

            "canonical_url":
                canonical_url,

            "landingpage_url":
                canonical_url,

            "robots_meta":
                robots_meta,

            "geo_verified":
                geo_verified,

            "related_products":
                self.build_related_products(
                    related_products
                ),

            "internal_links_html":
                self.build_internal_links(
                    product,
                    related_products
                ),

            "internal_links":
                self.link_optimizer.suggest_links(

                    {
                        "slug":
                            slug,

                        "category":
                            category
                    },

                    related_products

                ).get(
                    "links",
                    []
                ),

            "newsletter":
                f"""
<p>
Neue Ratgeber und Informationen zum Themenbereich
<strong>{escape(newsletter_segment)}</strong>
erhalten.
</p>

<a href="/newsletter">
Newsletter Anmeldung
</a>
""",

            "og_image_url":
                self.clean(
                    product.get(
                        "og_image_url"
                    )
                    or product.get(
                        "image_url"
                    )
                ),

            "footer":
                get_eeat_footer(),

            "cookie_consent":
                get_cookie_consent_script()
        }


    # =========================================================
    # RENDER
    # =========================================================

    def render(
        self,
        landingpage
    ):

        return self.renderer.render_landingpage(
            landingpage
        )


if __name__ == "__main__":

    builder = LandingPageBuilder()

    print(
        "LandingPageBuilder READY"
    )
