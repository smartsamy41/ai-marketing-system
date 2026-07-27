from datetime import datetime, timezone


class AIEvaluator:


    def evaluate(
        self,
        task,
        provider,
        response,
        validation,
        verification=None
    ):


        score = 0


        # Antwort vorhanden
        if response:

            score += 40


        # Validator bestanden
        if validation.get(
            "valid",
            False
        ):

            score += 30


        # Perplexity Prüfung vorhanden
        if verification:

            score += 20


        # Mindestlänge
        if len(
            str(response)
        ) > 200:

            score += 10



        return {

            "timestamp":
                datetime.now(
                    timezone.utc
                ).isoformat(),

            "task":
                task,

            "provider":
                provider,

            "score":
                score,

            "validation_status":
                validation.get(
                    "status"
                ),

            "verification":
                bool(
                    verification
                )

        }
