from engine.template_renderer import TemplateRenderer
from datetime import datetime, timezone
import json


class LandingpageBuilder:


    def __init__(
        self,
        system="FREE BASICS AI MARKETING SYSTEM"
    ):

        self.system = system
        self.renderer = TemplateRenderer()



    def build(
        self,
        product,
        facts=None,
        sources=None
    ):


        now = datetime.now(
            timezone.utc
        ).isoformat()



        product_id = product.get(
            "product_id",
            ""
        )


        name = product.get(
            "name",
            ""
        )



        summary = product.get(
            "summary",
            ""
        )



        return {


            "product_id":
                product_id,



            "title":
                product.get(
                    "hero_title",
                    name
                ),



            "description":
                summary,



            "canonical_url":
                product.get(
                    "landingpage_url",
                    f"https://freebasics.online/angebote/{product_id}"
                ),



            "product_name":
                name,



            "brand_name":
                product.get(
                    "partner",
                    ""
                ),



            "category":
                product.get(
                    "category",
                    ""
                ),



            "partner":
                product.get(
                    "partner",
                    ""
                ),



            "tracking_url":
                product.get(
                    "tracking_url",
                    "#"
                ),



            # KI Direktantwort
            "ai_summary":
                summary,



            # Kontext
            "introduction":
                (
                    f"Bei {name} spielen verschiedene Faktoren "
                    "eine Rolle. Dazu gehören Produktinformationen, "
                    "Vertragsbedingungen und relevante Merkmale."
                ),



            # Tiefere Informationen
            "content":
                (
                    f"Weitere Informationen zu {name} "
                    "basieren auf strukturierten Produktdaten "
                    "und dokumentierten Partnerinformationen."
                ),



            "sources":
                product.get(
                    "sources",
                    sources or []
                ),



            "faq":
                product.get(
                    "faq",
                    []
                ),



            "author":
                product.get(
                    "author",
                    "Redaktion Free Basics"
                ),



            "reviewed_by":
                product.get(
                    "reviewed_by",
                    "Samy ben Chedli Jendoubi"
                ),



            "updated_at":
                product.get(
                    "updated_at",
                    now
                ),



            "og_image_url":
                product.get(
                    "image_url",
                    "https://freebasics.online/assets/og-default.webp"
                ),



            "system":
                self.system



        }




    def render(
        self,
        landingpage
    ):


        schema = {


            "@context":
                "https://schema.org",



            "@type":
                "Product",



            "@id":
                landingpage.get(
                    "canonical_url",
                    ""
                )
                +
                "#product",



            "name":
                landingpage.get(
                    "title"
                ),



            "description":
                landingpage.get(
                    "description"
                ),



            "category":
                landingpage.get(
                    "category"
                ),



            "productID":
                landingpage.get(
                    "product_id"
                ),



            "brand":
                {
                    "@type":
                        "Organization",

                    "name":
                        landingpage.get(
                            "partner"
                        )
                }



        }



        return self.renderer.render(


            "landingpages/geo_optimized_landingpage.html",


            {


                **landingpage,



                "schema_json":

                    json.dumps(
                        schema,
                        indent=2,
                        ensure_ascii=False
                    )


            }


        )

