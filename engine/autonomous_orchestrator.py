from datetime import datetime

from engine.learning_logger import LearningLogger


class AutonomousOrchestrator:


    def __init__(
        self,
        autopilot,
        learning_loop,
        learning_logger=None
    ):

        self.autopilot = autopilot
        self.learning = learning_loop

        self.learning_logger = (
            learning_logger
            or LearningLogger()
        )


    # ========================================================
    # FULL SYSTEM CYCLE
    # ========================================================

    def run(self):


        # 1. AUTOPILOT ACTION

        result = self.autopilot.run()



        # 2. PERFORMANCE LEARNING

        learning = self.learning.optimize()



        # 3. WRITE LEARNING SIGNAL

        learning_log = None


        try:


            if learning.get("status") == "optimized":


                cycle_time = datetime.utcnow().strftime(
                    "%Y%m%d_%H%M%S"
                )



                learning_log = self.learning_logger.log_learning(


                    run_id=(
                        f"AUTONOMOUS_CYCLE_{cycle_time}"
                    ),


                    cycle_id=(
                        "ROUND_1"
                    ),


                    product_id=str(
                        learning.get(
                            "product",
                            "UNKNOWN"
                        )
                    ),


                    platform="AI_AGENT",


                    learning_type=(
                        "PERFORMANCE_OPTIMIZATION"
                    ),


                    signal=(
                        "BIGQUERY_TRAFFIC_SIGNAL"
                    ),


                    recommendation=learning.get(
                        "action",
                        "NO_ACTION"
                    ),


                    confidence=1.0,


                    status="LEARNED",



                    impressions=int(
                        learning.get(
                            "impressions",
                            0
                        )
                    ),


                    clicks=int(
                        learning.get(
                            "clicks",
                            0
                        )
                    ),


                    conversions=int(
                        learning.get(
                            "conversions",
                            0
                        )
                    ),


                    earnings=float(
                        learning.get(
                            "revenue",
                            0
                        )
                    ),


                    money_score=float(
                        learning.get(
                            "revenue",
                            0
                        )
                    ),


                    winner_status=False,


                    partner=learning.get(
                        "partner",
                        ""
                    ),


                    compliance_status=learning.get(
                        "compliance_status",
                        ""
                    ),


                    note=(
                        "Real BigQuery performance learning cycle"
                    )

                )



        except Exception as error:


            learning_log = {

                "status":
                    "ERROR",

                "error":
                    str(error)

            }



        # 4. RETURN SYSTEM RESULT


        return {


            "autopilot":
                result,


            "learning":
                learning,


            "learning_log":
                learning_log,


            "status":
                "CYCLE_COMPLETE"

        }
