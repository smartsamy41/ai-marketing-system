class VideoAssetSelector:


    def select(self, product_data):

        assets = product_data.get(
            "assets",
            []
        )


        # zuerst 300x250
        for asset in assets:

            html = str(
                asset.get(
                    "banner_300x250_html",
                    ""
                )
            )

            if html and html != "nan":

                return {
                    "type": "300x250",
                    "html": html
                }


        # fallback 728x90
        for asset in assets:

            html = str(
                asset.get(
                    "banner_728x90_html",
                    ""
                )
            )

            if html and html != "nan":

                return {
                    "type": "728x90",
                    "html": html
                }


        return {
            "type": "none",
            "html": ""
        }
