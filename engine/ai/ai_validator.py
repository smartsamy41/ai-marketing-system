class AIValidator:


    def validate(
        self,
        response
    ):

        result = {
            "status": "UNKNOWN",
            "valid": False,
            "length": 0,
            "issues": []
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
