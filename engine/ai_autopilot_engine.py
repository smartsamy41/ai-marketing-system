class AIAutopilotEngine:

    def __init__(self, sheets):

        self.sheets = sheets

    # =========================
    # DECISION ENGINE
    # =========================
    def decide(self):

        data = self.sheets.get_all()

        clicks = data["clicks"]

        score = {}

        for c in clicks:
            p = c["product"]
            score[p] = score.get(p, 0) + 1

        if not score:
            return {
                "action": "WAIT",
                "reason": "no data"
            }

        best = max(score, key=score.get)

        return {
            "action": "POST",
            "product": best,
            "reason": "highest engagement"
        }
