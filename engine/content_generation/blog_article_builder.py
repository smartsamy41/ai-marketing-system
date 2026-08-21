import json
from datetime import datetime, timezone

from engine.rendering.production_renderer import ProductionRenderer
from engine.self_learning_agent.internal_linking_optimizer import (
    InternalLinkingOptimizer
)

from app.templates.base_components import (
    get_eeat_footer,
    get_cookie_consent_script
)


class BlogArticleBuilder:

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
    def _normalize_partner(product):

        return str(
            product.get(
                "partner",
                ""
            )
            or ""
        ).strip().lower()


    @staticmethod
    def _normalize_product_id(product):

        return str(
            product.get(
                "product_id",
                ""
            )
            or ""
        ).strip()


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

        key_facts = (
            product.get(
                "key_facts",
                []
            )
            or []
        )

        comparison = (
            product.get(
                "comparison_matrix",
                []
            )
            or []
        )


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


        if key_facts:

            items = "\n".join(
                f"<li>{item}</li>"
                for item in key_facts
                if item
            )

            html.append(
                f"""
<section>

<h2>Welche Fakten sind wichtig?</h2>

<ul>
{items}
</ul>

</section>
"""
            )


        if comparison:

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


        extra_content = str(
            product.get(
                "content",
                ""
            )
            or ""
        ).strip()

        if extra_content:

            html.append(
                f"""
<section>

<h2>Weitere Informationen</h2>

<p>
{extra_content}
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

        if not summary:
            return ""

        return f"""
<p>
<strong>{name}:</strong>
{summary}
</p>
"""


    # =========================================================
    # ENTITY CONTEXT
    # =========================================================

    def _build_entity_context(
        self,
        product,
        facts=None
    ):

        category = str(
            product.get(
                "category",
                ""
            )
            or ""
        ).strip()

        partner = self._normalize_partner(
            product
        )

        silo = str(
            product.get(
                "silo",
                ""
            )
            or ""
        ).strip()

        cluster = str(
            product.get(
                "cluster",
                category
            )
            or ""
        ).strip()


        parts = []


        if silo:

            parts.append(
                f"""
<p>
<strong>Silo:</strong>
{silo}
</p>
"""
            )


        if cluster:

            parts.append(
                f"""
<p>
<strong>Cluster:</strong>
{cluster}
</p>
"""
            )


        if category:

            parts.append(
                f"""
<p>
<strong>Kategorie:</strong>
{category}
</p>
"""
            )


        if partner:

            parts.append(
                f"""
<p>
<strong>Partnerquelle:</strong>
{partner}
</p>
"""
            )


        parts.append(
            """
<p>
Die Inhalte basieren auf dem
Free-Basics-Knowledge-Layer und den
hinterlegten Produkt- und Partnerdaten.
</p>
"""
        )


        return "\n".join(
            parts
        )


    # =========================================================
    # SOURCES
    # =========================================================

    def _build_sources_html(
        self,
        sources
    ):

        html = []

        for source in sources or []:

            if isinstance(
                source,
                dict
            ):

                name = (
                    source.get("name")
                    or source.get("title")
                    or source.get("source")
                    or ""
                )

                url = str(
                    source.get(
                        "url",
                        ""
                    )
                    or ""
                ).strip()

                if url:

                    html.append(
                        f"""
<li>
<a href="{url}"
   target="_blank"
   rel="noopener">
{name or url}
</a>
</li>
"""
                    )

                elif name:

                    html.append(
                        f"<li>{name}</li>"
                    )

            elif source:

                html.append(
                    f"<li>{source}</li>"
                )


        return "\n".join(
            html
        )


    # =========================================================
    # FAQ
    # =========================================================

    def _build_faq_html(
        self,
        faq
    ):

        html = []

        for item in faq or []:

            if not isinstance(
                item,
                dict
            ):
                continue

            question = str(
                item.get(
                    "question",
                    ""
                )
                or ""
            ).strip()

            answer = str(
                item.get(
                    "answer",
                    ""
                )
                or ""
            ).strip()

            if not (
                question
                and answer
            ):
                continue

            html.append(
                f"""
<div class="faq-item">

<h3>{question}</h3>

<p>{answer}</p>

</div>
"""
            )


        return "\n".join(
            html
        )


    def _build_faq_schema(
        self,
        faq,
        canonical_url
    ):

        entities = []

        for item in faq or []:

            if not isinstance(
                item,
                dict
            ):
                continue

            question = str(
                item.get(
                    "question",
                    ""
                )
                or ""
            ).strip()

            answer = str(
                item.get(
                    "answer",
                    ""
                )
                or ""
            ).strip()

            if not (
                question
                and answer
            ):
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


        schema = {

            "@context":
                "https://schema.org",

            "@type":
                "FAQPage",

            "@id":
                canonical_url
                + "#faq",

            "mainEntity":
                entities

        }


        return json.dumps(
            schema,
            ensure_ascii=False,
            indent=2
        )


    # =========================================================
    # ARTICLE SCHEMA
    # =========================================================

    def _build_article_schema(
        self,
        article
    ):

        canonical = article.get(
            "canonical_url",
            ""
        )

        schema = {

            "@context":
                "https://schema.org",

            "@type":
                "Article",

            "@id":
                canonical
                + "#article",

            "mainEntityOfPage":
                canonical,

            "headline":
                article.get(
                    "title",
                    ""
                ),

            "description":
                article.get(
                    "description",
                    ""
                ),

            "author":
                {
                    "@type":
                        "Person",

                    "name":
                        article.get(
                            "author",
                            "Redaktion Free Basics"
                        )
                },

            "publisher":
                {
                    "@type":
                        "Organization",

                    "name":
                        "Free Basics",

                    "url":
                        "https://freebasics.online"
                },

            "dateModified":
                article.get(
                    "updated_at",
                    ""
                )

        }


        published_at = article.get(
            "published_at"
        )

        if published_at:

            schema[
                "datePublished"
            ] = published_at


        return json.dumps(
            schema,
            ensure_ascii=False,
            indent=2
        )


    # =========================================================
    # RELATED CONTENT
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

                slug = self._slugify(
                    name
                )

                url = (
                    "/angebote/"
                    + slug
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

        slug = self._slugify(
            category
            or product.get(
                "name",
                ""
            )
        )


        try:

            result = (
                self.link_optimizer
                .suggest_links(
                    {
                        "slug":
                            slug,

                        "category":
                            category
                    },

                    related_products
                    or []
                )
            )

        except Exception:

            result = {}


        links = result.get(
            "links",
            []
        )


        html = []

        for link in links or []:

            if isinstance(
                link,
                dict
            ):

                url = (
                    link.get("url")
                    or link.get("href")
                    or ""
                )

                label = (
                    link.get("title")
                    or link.get("name")
                    or url
                )

            else:

                url = str(
                    link
                )

                label = url


            if not url:
                continue


            html.append(
                f"""
<p>
<a href="{url}">
{label}
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

        partner = self._normalize_partner(
            product
        )

        product_id = self._normalize_product_id(
            product
        )

        tracking_url = str(
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


        # -----------------------------------------------------
        # TELEKOM
        # -----------------------------------------------------

        if (
            partner == "telekom"
            or product_id.startswith(
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
Das Angebot und die weitere Abwicklung
erfolgen im Telekom-Profis-Shop.
</p>

<a href="{target}"
   target="_blank"
   rel="sponsored nofollow noopener">

Zum Telekom-Profis-Shop

</a>

</div>
"""


        # -----------------------------------------------------
        # AMAZON
        # -----------------------------------------------------

        if partner == "amazon":

            target = (
                tracking_url
                or landingpage
            )

            if not target:
                return ""

            return f"""
<div class="official-affiliate-asset">

<p>
<strong>Werbung / Anzeige</strong>
</p>

<a href="{target}"
   target="_blank"
   rel="sponsored nofollow noopener">

Bei Amazon ansehen

</a>

</div>
"""


        # -----------------------------------------------------
        # CHECK24 / TARIFCHECK / OTHER
        # -----------------------------------------------------

        target = (
            tracking_url
            or landingpage
        )

        if not target:
            return ""


        extra = ""

        if partner == "tarifcheck":

            extra = """
<p>
powered by TARIFCHECK24 GmbH
</p>
"""


        return f"""
<div class="official-affiliate-asset">

<p>
<strong>Werbung / Anzeige</strong>
</p>

{extra}

<a href="{target}"
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
        facts=None,
        related_products=None
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


        summary = str(
            product.get(
                "summary",
                ""
            )
            or ""
        ).strip()


        slug = self._slugify(
            product.get(
                "article_slug",
                f"{name}-ratgeber"
            )
        )


        canonical_url = str(
            product.get(
                "article_url",
                ""
            )
            or ""
        ).strip()


        if not canonical_url:

            category_slug = self._slugify(
                product.get(
                    "category",
                    ""
                )
            )

            if category_slug:

                canonical_url = (
                    "https://freebasics.online/"
                    f"blog/{category_slug}-ratgeber"
                )

            else:

                canonical_url = (
                    "https://freebasics.online/"
                    f"blog/{slug}"
                )


        faq = (
            product.get(
                "faq",
                []
            )
            or []
        )


        sources = (
            product.get(
                "sources",
                []
            )
            or []
        )


        article = {

            "system":
                self.system,

            "product_id":
                self._normalize_product_id(
                    product
                ),

            "title":
                name,

            "description":
                summary,

            "ai_summary":
                summary,

            "direct_answer":
                self._build_direct_answer(
                    product
                ),

            "content":
                self._build_content(
                    product
                ),

            "entity_context":
                self._build_entity_context(
                    product,
                    facts=facts
                ),

            "sources":
                self._build_sources_html(
                    sources
                ),

            "questions":
                self._build_faq_html(
                    faq
                ),

            "faq":
                self._build_faq_html(
                    faq
                ),

            "related_products":
                self._build_related_products_html(
                    related_products
                    or []
                ),

            "internal_links":
                self._build_internal_links(
                    product,
                    related_products
                    or []
                ),

            "affiliate_area":
                self._build_affiliate_area(
                    product
                ),

            "newsletter":
                """
<p>
Neue Ratgeber und Informationen von Free Basics erhalten.
</p>
""",

            "footer":
                get_eeat_footer(),

            "canonical_url":
                canonical_url,

            "article_url":
                canonical_url,

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

            "published_at":
                product.get(
                    "published_at",
                    ""
                ),

            "updated_at":
                product.get(
                    "updated_at",
                    now
                ),

            "og_image_url":
                product.get(
                    "og_image_url",
                    ""
                ),

            "og_image_meta":
                self._build_og_image_meta(
                    product
                ),

            "cookie_consent":
                get_cookie_consent_script()

        }


        article[
            "article_schema"
        ] = self._build_article_schema(
            article
        )


        article[
            "faq_schema"
        ] = self._build_faq_schema(
            faq,
            canonical_url
        )


        return article


    # =========================================================
    # RENDER
    # =========================================================

    def render(
        self,
        article
    ):

        return self.renderer.renderer.render(
            "blog/geo_authority_article.html",
            article
        )
