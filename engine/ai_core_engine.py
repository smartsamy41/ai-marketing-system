from engine.learning_reader import LearningReader


class AICoreEngine:

    def __init__(self, sheets_api):

        self.sheets = sheets_api
        self.learning = LearningReader()


    # =========================
    # FULL ANALYSIS LOOP
    # =========================

    def run_analysis(self):

        data = self.sheets.export()

        clicks = data.get(
            "clicks",
            []
        )

        conversions = data.get(
            "conversions",
            []
        )


        score = {}


        for c in clicks:

            product = c.get(
                "product"
            )

            if product:

                score[product] = (
                    score.get(product, 0)
                    + 1
                )


        revenue = 0


        for c in conversions:

            revenue += float(
                c.get(
                    "value",
                    0
                )
            )


        top = sorted(
            score.items(),
            key=lambda x: x[1],
            reverse=True
        )


        return {

            "clicks":
                len(clicks),

            "conversions":
                len(conversions),

            "revenue":
                revenue,

            "top_products":
                top

        }


    # =========================
    # LEARNING ANALYSIS
    # =========================

    def get_learning_priority(self):

        winners = self.learning.get_winners()

        if not winners:

            return None


        return winners[0]


    # =========================
    # AUTO DECISION ENGINE
    # =========================

    def decide_next_action(self):

        learning = self.get_learning_priority()


        # ROUND 2:
        # Gewinner aus Learning bevorzugen

        if learning:

            return {

                "action":
                    "PUBLISH",

                "product":
                    learning["product_id"],

                "reason":
                    "learning_winner_priority",

                "cycle":
                    "ROUND_2"

            }


        # ROUND 1:
        # normale Datensammlung

        analysis = self.run_analysis()


        if analysis["clicks"] < 3:

            return {

                "action":
                    "WAIT",

                "reason":
                    "not enough data",

                "cycle":
                    "ROUND_1"

            }


        if not analysis["top_products"]:

            return {

                "action":
                    "WAIT",

                "reason":
                    "no products yet",

                "cycle":
                    "ROUND_1"

            }


        best = analysis["top_products"][0][0]


        return {

            "action":
                "PUBLISH",

            "product":
                best,

            "reason":
                "highest performance detected",

            "cycle":
                "ROUND_1"

        }
