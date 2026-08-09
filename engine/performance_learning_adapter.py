class PerformanceLearningAdapter:

    def __init__(self, ai_core):
        self.ai = ai_core


    def optimize(self):

        analysis = self.ai.run_analysis()

        if analysis["clicks"] == 0:
            return {
                "status": "no_data"
            }


        products = analysis.get(
            "top_products",
            []
        )


        if not products:

            return {
                "status": "no_data"
            }


        product = products[0][0]


        return {

            "status": "optimized",

            "action": "BOOST_PRODUCT",

            "product": product,

            "revenue": analysis.get(
                "revenue",
                0
            ),

            "clicks": analysis.get(
                "clicks",
                0
            ),

            "conversions": analysis.get(
                "conversions",
                0
            )

        }
