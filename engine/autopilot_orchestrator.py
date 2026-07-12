from engine.cycle_manager import CycleManager
from engine.cycle_logger import CycleLogger
from engine.learning_reader import LearningReader


class AutopilotOrchestrator:

    def __init__(
        self,
        ai,
        content,
        sheets,
        yt,
        pin,
        revenue,
        affiliate=None,
        compliance=None,
        winner_engine=None
    ):

        self.ai = ai
        self.content = content
        self.sheets = sheets
        self.youtube = yt
        self.pinterest = pin
        self.revenue = revenue
        self.affiliate = affiliate
        self.compliance = compliance

        # Learning Loop
        self.cycle_manager = CycleManager()
        self.cycle_logger = CycleLogger()
        self.learning_reader = LearningReader()

        # Winner Gate
        self.winner_engine = winner_engine


    def run(self):

        decision = self.ai.decide_next_action()


        if decision.get("action") == "WAIT":

            return {
                "status": "WAIT",
                "reason": decision.get("reason")
            }


        product = decision.get("product")


        if not product:

            return {
                "status": "BLOCKED",
                "reason": "MISSING_PRODUCT"
            }


        if isinstance(product, dict):

            product_id = (
                product.get("product_id")
                or product.get("id")
                or "UNKNOWN_PRODUCT"
            )

        else:

            product_id = str(product)



        cycle = self.cycle_manager.create_run(
            product_id=product_id,
            platform="CONTENT",
            cycle_id="ROUND_1"
        )


        if cycle.get("status") == "BLOCKED":

            return cycle



        self.cycle_logger.log_run(
            run_id=cycle["run_id"],
            cycle_id=cycle["cycle_id"],
            product_id=cycle["product_id"],
            platform=cycle["platform"],
            status="PROCESSING",
            note="Autopilot cycle started"
        )


        generated_content = self.content.generate(
            product
        )


        compliance_result = {

            "status": "NOT_CONFIGURED",
            "errors": [],
            "partner_rules": []

        }


        partner = None


        if self.affiliate:

            product_data = self.affiliate.get_product_data(
                product
            )

            if product_data.get("status") == "FOUND":

                partner = product_data.get(
                    "source"
                )



        if self.compliance:

            compliance_result = self.compliance.audit(
                generated_content,
                partner=partner
            )


            if compliance_result.get("status") == "BLOCKED":


                self.cycle_logger.log_run(

                    run_id=cycle["run_id"],

                    cycle_id=cycle["cycle_id"],

                    product_id=cycle["product_id"],

                    platform=cycle["platform"],

                    status="BLOCKED",

                    note="Compliance failed"

                )


                return {

                    "status": "BLOCKED",

                    "reason": "COMPLIANCE_FAILED",

                    "audit": compliance_result

                }



        winner_result = {

            "winner_status": False,
            "video_allowed": False,
            "voice_allowed": False,
            "reason": "NO_WINNER_ENGINE"

        }


        if self.winner_engine:


            learning_data = (
                self.learning_reader.get_product_learning(
                    product_id
                )
            )


            if learning_data:

                money_score = float(
                    learning_data.get(
                        "money_score",
                        0
                    )
                    or 0
                )

                ctr = float(
                    learning_data.get(
                        "ctr",
                        0
                    )
                    or 0
                )

                conversions = int(
                    learning_data.get(
                        "conversions",
                        0
                    )
                    or 0
                )

                earnings = float(
                    learning_data.get(
                        "earnings",
                        0
                    )
                    or 0
                )


            else:

                money_score = 0
                ctr = 0
                conversions = 0
                earnings = 0



            winner_result = self.winner_engine.evaluate(

                money_score=money_score,

                ctr=ctr,

                conversions=conversions,

                earnings=earnings,

                compliance_status=
                    compliance_result.get(
                        "status",
                        "OK"
                    )

            )



        affiliate_link = None
        tracking_link = None
        product_data = None


        if self.affiliate:

            product_data = self.affiliate.get_product_data(
                product
            )


            if product_data.get("status") == "FOUND":

                affiliate_link = product_data.get(
                    "affiliate_url"
                )

                tracking_link = product_data.get(
                    "tracking_url"
                )



        youtube_result = {

            "status": (

                "WINNER_APPROVED"

                if winner_result.get(
                    "video_allowed"
                )

                else "NOT_ALLOWED"

            ),

            "voice_allowed":
                winner_result.get(
                    "voice_allowed"
                ),

            "reason":
                winner_result.get(
                    "reason"
                )

        }


        pinterest_result = {

            "status":
                "waiting_for_image_asset"

        }



        return {

            "status": "READY",

            "run_id": cycle["run_id"],

            "cycle_id": cycle["cycle_id"],

            "product_id": cycle["product_id"],

            "product": product,

            "content": generated_content,

            "partner": partner,

            "affiliate_link": affiliate_link,

            "tracking_link": tracking_link,

            "product_data": product_data,

            "compliance": compliance_result,

            "winner": winner_result,

            "youtube": youtube_result,

            "pinterest": pinterest_result,

            "revenue": self.revenue.stats()

        }
