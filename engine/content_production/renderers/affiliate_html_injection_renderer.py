import json
from pathlib import Path
from datetime import datetime, timezone


class AffiliateHTMLInjectionRenderer:


    def __init__(self):

        self.primary_file = Path(
            "data_master/content_production/primary_asset_selection/primary_asset_selection_graph.json"
        )

        self.asset_file = Path(
            "data_master/content_intelligence/affiliate_asset_knowledge_graph.json"
        )

        self.source_pages = Path(
            "data_master/content_production/generated_pages"
        )

        self.output_pages = Path(
            "data_master/content_production/final_pages"
        )



    def load_json(self, path):

        with open(
            path,
            encoding="utf-8"
        ) as f:

            return json.load(f)



    def load_primary(self):

        data = self.load_json(
            self.primary_file
        )

        return data["products"]



    def load_assets(self):

        data = self.load_json(
            self.asset_file
        )

        assets = {}

        for asset in data["assets"]:

            assets[
                asset["asset_id"]
            ] = asset


        return assets



    def get_asset_html(self, asset):


        source = asset.get(
            "source",
            ""
        )


        if source == "Vergleichsrechner/Formular":

            return asset.get(
                "calculator",
                ""
            )


        if source == "Kurzrechner":

            return asset.get(
                "short_calculator",
                ""
            )


        if source == "Banner 300x250":

            return asset.get(
                "banner_300x250",
                ""
            )


        if source == "Banner 728x90":

            return asset.get(
                "banner_728x90",
                ""
            )


        if source == "Direktlink":

            return f"""
<a href="{asset.get('direct_link','')}" target="_blank">
Vergleich starten
</a>
"""


        return ""



    def create_block(
        self,
        product
    ):


        asset_id = product["primary_asset"]["asset_id"]


        asset = self.assets.get(
            asset_id,
            {}
        )


        html = self.get_asset_html(
            asset
        )


        return f"""

<section class="affiliate-box">

<h2>
Werbung / Anzeige
</h2>

<div class="affiliate-content">

{html}

</div>

</section>

"""



    def clean_old_blocks(
        self,
        html
    ):


        start = '<section class="affiliate-box">'

        end = "</section>"


        while start in html:


            s = html.find(start)


            e = html.find(
                end,
                s
            )


            if e == -1:
                break


            e += len(end)


            html = (
                html[:s]
                +
                html[e:]
            )


        return html



    def run(self):


        products = self.load_primary()


        self.assets = self.load_assets()



        self.output_pages.mkdir(
            parents=True,
            exist_ok=True
        )


        count = 0



        for product_id, product in products.items():


            source = (
                self.source_pages /
                f"{product_id}.html"
            )


            if not source.exists():

                continue



            html = source.read_text(
                encoding="utf-8"
            )



            html = self.clean_old_blocks(
                html
            )



            block = self.create_block(
                product
            )



            if "</body>" in html:


                html = html.replace(
                    "</body>",
                    block +
                    "\n</body>"
                )


            else:

                html += block



            target = (

                self.output_pages /
                f"{product_id}.html"

            )


            target.write_text(
                html,
                encoding="utf-8"
            )


            count += 1



        status = {


            "system":
            "FREE BASICS AI MARKETING SYSTEM",


            "version":
            "AFFILIATE_HTML_INJECTION_V2",


            "pages":
            count,


            "assets_loaded":
            len(self.assets),


            "time":
            datetime.now(
                timezone.utc
            ).isoformat()

        }



        (
            self.output_pages /
            "affiliate_html_status.json"
        ).write_text(

            json.dumps(
                status,
                indent=2,
                ensure_ascii=False
            ),

            encoding="utf-8"

        )



        print(
            "AFFILIATE HTML INJECTION V2 CREATED"
        )

        print(
            "PAGES:",
            count
        )

        print(
            "ASSETS:",
            len(self.assets)
        )



if __name__=="__main__":

    AffiliateHTMLInjectionRenderer().run()
