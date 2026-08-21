from datetime import datetime, timezone

from engine.rendering.production_renderer import ProductionRenderer
from engine.self_learning_agent.internal_linking_optimizer import (
    InternalLinkingOptimizer
)

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


    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _slugify(text):

        return (
            str(text or "")
            .strip()
            .lower()
            .replace(" ", "-")
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .replace("ß", "ss")
        )


    @staticmethod
    def _partner(product):

        return str(
            product.get(
                "partner",
                ""
            )
            or ""
        ).strip().lower()


    def _build_og_image_meta(
        self,
        product
    ):

        url = str(
            product.get(
                "og_image_url",
                ""
            )
            or ""
        ).strip()

        if not url:
            return ""

        return (
            f'<meta property="og:image" content="{url}">\n'
            f'<meta name="twitter:image" content="{url}">'
        )


    # =========================================================
    # CONTENT
    # =========================================================

    def _build_content(
        self,
        product
    ):

        html = []

        name = str(
            product.get(
                "name",
                product.get(
                    "product_name",
                    "Produkt"
                )
            )
            or ""
        ).strip()

        summary = str(
            product.get(
                "summary",
                ""
            )
            or ""
        ).strip()


        if summary:

            html.append(
                f"""
<section>

<h2>Worum geht es bei {name}?</h2>

<p>
{summary}
</p>

</section>
"""
            )


        facts = (
            product.get(
                "key_facts",
                []
            )
            or []
        )


        if facts:

            fact_html = "\n".join(
                f"<li>{fact}</li>"
                for fact in facts
                if fact
            )

            html.append(
                f"""
<section>

<h2>Welche Fakten sind wichtig?</h2>

<ul>
{fact_html}
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


        rows = []

        for item in comparison:

            if not isinstance(
                item,
                dict
            ):
                continue

            field = item.get(
                "field",
                ""
            )

            value = item.get(
                "value",
                ""
            )

            if not (
                field
                or value
            ):
                continue


            rows.append(
                f"""
<tr>
<th>{field}</th>
<td>{value}</td>
</tr>
"""
            )


        if rows:

            html.append(
                f"""
<section>

<h2>Welche Daten sollten verglichen werden?</h2>

<table>

<tbody>
{''.join(rows)}
</tbody>

</table>

</section>
"""
            )


        extra = str(
            product.get(
                "content",
                ""
            )
            or ""
        ).strip()


        if extra:

            html.append(
                f"""
<section>

<h2>Weitere Informationen</h2>

<p>
{extra}
</p>

</section>
"""
            )


        return "\n".join(
            html
        )


    # =========================================================
    # DIRECT ANSWER
    # =========================================================

    def _build_direct_answer(
        self,
        product
    ):

        name = str(
            product.get(
                "name",
                "Produkt"
            )
            or "Produkt"
        ).strip()

        summary = str(
            product.get(
                "summary",
                ""
            )
            or ""
        ).strip()

        if not summary:
            return ""

        return f"""
<p>
<strong>{name}:</strong>
{summary}
</p>
"""


    # =========================================================
    # RELATED PRODUCTS
    # =========================================================

    def _build_related_products_html(
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

            name = (
                item.get("name")
                or item.get("category")
                or item.get("product_id")
                or ""
            )


            if not name:
                continue


            url = str(
                item.get(
                    "landingpage",
                    ""
                )
                or ""
            ).strip()


            if not url:

                url = (
                    "/angebote/"
                    + self._slugify(
                        name
                    )
                )


            html.append(
                f"""
<div class="related-product">

<a href="{url}">
{name}
</a>

</div>
"""
            )


        return "\n".join(
            html
        )


    # =========================================================
    # INTERNAL LINKS
    # =========================================================

    def _build_internal_links(
        self,
        product,
        related_products
    ):

        category = str(
            product.get(
                "category",
                ""
            )
            or ""
        ).strip()


        try:

            result = (
                self.link_optimizer
                .suggest_links(
                    {
                        "slug":
                            self._slugify(
                                category
                            ),

                        "category":
                            category
                    },

                    related_products
                    or []
                )
            )

        except Exception:

            return ""


        links = (
            result.get(
                "links",
                []
            )
            or []
        )


        html = []


        for link in links:

            if isinstance(
                link,
                dict
            ):

                url = (
                    link.get("url")
                    or link.get("href")
                    or ""
                )

                title = (
                    link.get("title")
                    or link.get("name")
                    or url
                )

            else:

                url = str(
                    link
                )

                title = url


            if url:

                html.append(
                    f"""
<p>
<a href="{url}">
{title}
</a>
</p>
"""
                )


        return "\n".join(
            html
        )


    # =========================================================
    # AFFILIATE AREA
    # =========================================================

    def _build_affiliate_area(
        self,
        product
    ):

        partner = self._partner(
            product
        )

        pid = str(
            product.get(
                "product_id",
                ""
            )
            or ""
        )


        tracking = str(
            product.get(
                "tracking_url",
                ""
            )
            or ""
        ).strip()


        landingpage = str(
            product.get(
                "landingpage",
                ""
            )
            or ""
        ).strip()


        shop_url = str(
            product.get(
                "shop_url",
                ""
            )
            or ""
        ).strip()


        conversion_target = str(
            product.get(
                "conversion_target",
                ""
            )
            or ""
        ).strip()


        # TELEKOM
        if (
            partner == "telekom"
            or pid.startswith(
                "TEL_"
            )
            or conversion_target
            == "external_shop"
        ):

            target = (
                shop_url
                or landingpage
                or "https://free-basics.telekom-profis.de"
            )

            return f"""
<div class="official-affiliate-asset">

<p>
<strong>Werbung / Anzeige</strong>
</p>

<p>
Die weitere Produktinformation und Abwicklung
erfolgt im Telekom-Profis-Shop.
</p>

<a class="button"
   href="{target}"
   target="_blank"
   rel="sponsored nofollow noopener">

Zum Telekom-Profis-Shop

</a>

</div>
"""


        # AMAZON
        if partner == "amazon":

            target = (
                tracking
                or landingpage
            )

            if not target:
                return ""

            return f"""
<div class="official-affiliate-asset">

<p>
<strong>Werbung / Anzeige</strong>
</p>

<a class="button"
   href="{target}"
   target="_blank"
   rel="sponsored nofollow noopener">

Bei Amazon ansehen

</a>

</div>
"""


        # TARIFCHECK
        if partner == "tarifcheck":

            target = (
                tracking
                or landingpage
            )

            if not target:
                return ""

            return f"""
<div class="official-affiliate-asset">

<p>
<strong>Werbung / Anzeige</strong>
</p>

<p>
powered by TARIFCHECK24 GmbH
</p>

<a class="button"
   href="{target}"
   target="_blank"
   rel="sponsored nofollow noopener">

Vergleich starten

</a>

</div>
"""


        # CHECK24 / fallback
        target = (
            tracking
            or landingpage
        )

        if not target:
            return ""


        return f"""
<div class="official-affiliate-asset">

<p>
<strong>Werbung / Anzeige</strong>
</p>

<a class="button"
   href="{target}"
   target="_blank"
   rel="sponsored nofollow noopener">

Vergleich starten

</a>

</div>
"""


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
        ).isoformat()


        name = str(
            product.get(
                "name",
                product.get(
                    "product_name",
                    "Produkt"
                )
            )
            or "Produkt"
        ).strip()


        category = str(
            product.get(
                "category",
                ""
            )
            or ""
        ).strip()


        partner = self._partner(
            product
        )


        slug = self._slugify(
            name
        )


        canonical_url = str(
            product.get(
                "landingpage",
                ""
            )
            or ""
        ).strip()


        if (
            partner == "telekom"
            or str(
                product.get(
                    "conversion_target",
                    ""
                )
            ) == "external_shop"
        ):

            canonical_url = (
                "https://freebasics.online/"
                f"blog/{slug}"
            )

        elif not canonical_url:

            canonical_url = (
                "https://freebasics.online/"
                f"angebote/{slug}"
            )


        internal_links = self._build_internal_links(
            product,
            related_products
            or []
        )


        return {

            "system":
                self.system,

            "product_id":
                product.get(
                    "product_id",
                    ""
                ),

            "title":
                name,

            "category":
                category,

            "partner":
                partner,

            "description":
                product.get(
                    "summary",
                    ""
                ),

            "direct_answer":
                self._build_direct_answer(
                    product
                ),

            "content":
                self._build_content(
                    product
                ),

            "faq":
                product.get(
                    "faq",
                    []
                ),

            "questions":
                product.get(
                    "questions",
                    []
                ),

            "sources":
                product.get(
                    "sources",
                    []
                ),

            "tracking_url":
                product.get(
                    "tracking_url",
                    ""
                ),

            "affiliate_area":
                self._build_affiliate_area(
                    product
                ),

            "author":
                product.get(
                    "author",
                    "Redaktion Free Basics"
                ),

            "reviewed_by":
                product.get(
                    "reviewed_by",
                    ""
                ),

            "updated_at":
                product.get(
                    "updated_at",
                    now
                ),

            "canonical_url":
                canonical_url,

            "related_products":
                self._build_related_products_html(
                    related_products
                    or []
                ),

            "internal_links":
                internal_links,

            "og_image_url":
                product.get(
                    "og_image_url",
                    ""
                ),

            "og_image_meta":
                self._build_og_image_meta(
                    product
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
