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

        validation_status = (
            validation.get(
                "status",
                "UNKNOWN"
            )
        )

        provider_error = bool(
            validation.get(
                "provider_error",
                False
            )
        )


        # =====================================================
        # PROVIDER ERROR
        # =====================================================

        if (
            provider_error
            or validation_status == "ERROR"
        ):

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
                    0,

                "validation_status":
                    "ERROR",

                "verification":
                    False,

                "provider_error":
                    True
            }


        score = 0


        # =====================================================
        # RESPONSE PRESENT
        # =====================================================

        if response:

            score += 40


        # =====================================================
        # VALIDATOR PASSED
        # =====================================================

        if validation.get(
            "valid",
            False
        ):

            score += 30


        # =====================================================
        # VERIFICATION PRESENT
        # =====================================================

        if verification:

            score += 20


        # =====================================================
        # RESPONSE DEPTH
        # =====================================================

        if len(
            str(
                response or ""
            )
        ) > 200:

            score += 10


        # =====================================================
        # FINAL RESULT
        # =====================================================

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
                validation_status,

            "verification":
                bool(
                    verification
                ),

            "provider_error":
                False
        }
