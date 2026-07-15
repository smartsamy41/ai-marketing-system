from engine.learning_reader import LearningReader
from engine.performance_reader import PerformanceReader


class AICoreEngine:

    def __init__(self, sheets_api):

        self.sheets = sheets_api
        self.performance = PerformanceReader()
        self.learning = LearningReader()


    # =========================
    # FULL ANALYSIS LOOP
    # =========================

    def run_analysis(self):

        try:

            performance = self.performance.get_summary()

            clicks = performance.get(
                "clicks",
                []
            )

            conversions = performance.get(
                "conversions",
                []
            )

            earnings = performance.get(
                "earnings",
                []
            )


        except Exception:

            data = self.sheets.export()

            clicks = data.get(
                "clicks",
                []
            )

            conversions = data.get(
                "conversions",
                []
            )

            earnings = []


        score = {}


        for item in clicks:

            product = item.get(
                "product_id"
            )


            if product:

                score[product] = (
                    score.get(product, 0)
                    + int(
                        item.get(
                            "clicks",
                            0
                        )
                    )
                )


        revenue = 0


        for item in earnings:

            revenue += float(
                item.get(
                    "earnings",
                    0
                )
                or 0
            )


        top_products = sorted(
            score.items(),
            key=lambda x: x[1],
            reverse=True
        )


        return {

            "clicks":
                sum(score.values()),

            "conversions":
                len(conversions),

            "revenue":
                revenue,

            "top_products":
                top_products

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
