from engine.learning_logger import LearningLogger


class AILearningBridge:


    def __init__(
        self,
        project_id="smartcontent2050",
        dataset="smartcontent"
    ):

        self.logger = LearningLogger(
            project_id=project_id,
            dataset=dataset
        )


    def log_ai_result(
        self,
        task,
        provider,
        score,
        validation_status,
        verification=False
    ):

        recommendation = self.get_recommendation(
            task,
            provider,
            score,
            validation_status
        )


        if validation_status == "ERROR":

            learning_status = "ERROR"

        elif validation_status == "FAILED":

            learning_status = "FAILED"

        elif validation_status == "WARNING":

            learning_status = "WARNING"

        else:

            learning_status = "ACTIVE"


        return self.logger.log_learning(

            run_id="AI_PROVIDER_RUN",

            cycle_id="AI_LEARNING",

            product_id="AI_CORE",

            platform=provider,

            learning_type="AI_PROVIDER",

            signal=f"{task}_quality_score",

            recommendation=recommendation,

            confidence=(
                float(score) / 100
            ),

            status=learning_status,

            note=(
                f"validation={validation_status}; "
                f"verification={verification}; "
                f"score={score}"
            )
        )


    def get_recommendation(
        self,
        task,
        provider,
        score,
        validation_status
    ):

        if validation_status in {
            "ERROR",
            "FAILED"
        }:

            return (
                f"DISABLE_OR_REVIEW_{provider.upper()}_FOR_{task.upper()}"
            )


        if score >= 90:

            return (
                f"USE_{provider.upper()}_FOR_{task.upper()}"
            )


        if score >= 70:

            return (
                f"KEEP_{provider.upper()}_AVAILABLE"
            )


        return (
            f"REVIEW_{provider.upper()}"
        )
