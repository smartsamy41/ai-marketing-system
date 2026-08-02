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


    # =========================
    # FULL SYSTEM CYCLE
    # =========================
    def run(self):

        # 1. AI ACTION
        result = self.autopilot.run()


        # 2. LEARNING STEP
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
                        "WINNER_PRODUCT_DETECTED"
                    ),

                    recommendation=learning.get(
                        "action",
                        "NO_ACTION"
                    ),

                    confidence=1.0,

                    status="LEARNED",

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

                    winner_status=True,

                    note=(
                        "Autonomous learning cycle"
                    )
                )


        except Exception as error:

            learning_log = {

                "status": "ERROR",

                "error": str(error)

            }



        # 4. MERGE INTELLIGENCE
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
