class AIValidator:

    ERROR_PREFIXES = (
        "OPENAI_ERROR:",
        "GEMINI_ERROR:",
        "GROQ_ERROR:",
        "PERPLEXITY_ERROR:",
        "HUGGINGFACE_ERROR:",
        "HF_ERROR:",
        "AI_ERROR:"
    )


    def validate(
        self,
        response
    ):

        result = {
            "status": "UNKNOWN",
            "valid": False,
            "length": 0,
            "issues": [],
            "provider_error": False
        }


        if response is None:

            result["issues"].append(
                "empty_response"
            )

            result["status"] = "FAILED"

            return result


        text = str(
            response
        ).strip()


        if not text:

            result["issues"].append(
                "blank_text"
            )

            result["status"] = "FAILED"

            return result


        result["length"] = len(
            text
        )


        upper_text = text.upper()


        if upper_text.startswith(
            self.ERROR_PREFIXES
        ):

            result["issues"].append(
                "provider_error"
            )

            result["provider_error"] = True

            result["status"] = "ERROR"

            return result


        if len(text) < 20:

            result["issues"].append(
                "response_too_short"
            )


        if not result["issues"]:

            result["status"] = "VALID"
            result["valid"] = True

        else:

            result["status"] = "WARNING"


        return result
