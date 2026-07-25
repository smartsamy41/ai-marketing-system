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
        ).strftime("%Y-%m-%d")



        return {


            "product_id":
                product.get(
                    "product_id",
                    ""
                ),



            "title":
                product.get(
                    "hero_title",
                    product.get(
                        "name",
                        ""
                    )
                ),



            "description":
                product.get(
                    "summary",
                    f"Informationen zu {product.get('name','Produkt')}"
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



            "ai_summary":
                product.get(
                    "summary",
                    ""
                ),



            "introduction":
                product.get(
                    "summary",
                    ""
                ),



            "content":
                product.get(
                    "content",
                    ""
                ),



            "key_facts":
                product.get(
                    "key_facts",
                    []
                ),



            "comparison_matrix":
                product.get(
                    "comparison_matrix",
                    []
                ),



            "facts":
                facts or {},



            "sources":
                product.get(
                    "sources",
                    sources or []
                ),



            "internal_links":
                product.get(
                    "internal_links",
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



            "faq":
                product.get(
                    "faq",
                    []
                ),



            "methodology":
                "Die Inhalte basieren auf strukturierten Produktdaten, "
                "offiziellen Quellen und dokumentierten Datenmodellen.",



            "type":
                "landingpage",



            "status":
                "ready_for_render",



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



            "name":
                landingpage.get(
                    "title"
                ),



            "category":
                landingpage.get(
                    "category"
                ),



            "productID":
                landingpage.get(
                    "product_id"
                )

        }



        return self.renderer.render(

            "landingpages/geo_optimized_landingpage.html",

            {

                **landingpage,


                "canonical_url":
                    f"https://freebasics.online/angebote/{landingpage['product_id']}",



                "schema_json":
                    json.dumps(
                        schema,
                        indent=2,
                        ensure_ascii=False
                    )

            }

        )




    def validate(
        self,
        landingpage
    ):


        required = [

            "product_id",
            "title",
            "partner",
            "author",
            "reviewed_by",
            "updated_at"

        ]



        missing = [

            field

            for field in required

            if not landingpage.get(field)

        ]



        return {

            "valid":
                len(missing) == 0,


            "missing":
                missing

        }



if __name__ == "__main__":


    builder = LandingpageBuilder()


    page = builder.build(

        {

            "product_id":
                "CHK24_001",

            "name":
                "Strom",

            "category":
                "Energie",

            "partner":
                "check24"

        }

    )


    print(

        builder.validate(
            page
        )

    )


    print(

        builder.render(
            page
        )[:500]

    )
