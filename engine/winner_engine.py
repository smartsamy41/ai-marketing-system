class WinnerEngine:


    def evaluate(
        self,
        money_score: float,
        ctr: float,
        conversions: int,
        earnings: float,
        compliance_status: str
    ):


        if compliance_status != "OK":

            return {
                "winner_status": False,
                "video_allowed": False,
                "voice_allowed": False,
                "reason": "COMPLIANCE_FAILED"
            }


        score = 0


        if money_score >= 70:
            score += 1


        if ctr >= 0.05:
            score += 1


        if conversions >= 3:
            score += 1


        if earnings > 0:
            score += 1


        winner = score >= 3


        return {

            "winner_status": winner,

            "video_allowed": winner,

            "voice_allowed": winner,

            "score": score,

            "reason":
                "WINNER_PRODUCT"
                if winner
                else "NOT_ENOUGH_DATA"

        }
