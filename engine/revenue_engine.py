class RevenueEngine:

    def __init__(self):
        self.stats = {
            "offen": 0,
            "bestätigt": 0,
            "vergütet": 0,
            "storniert": 0,
            "revenue": 0.0
        }

    # =========================
    # PROCESS SALES
    # =========================
    def process_leads(self, leads):

        for lead in leads:

            status = lead.get("status")
            amount = float(lead.get("amount_net", 0))

            if status == "offen":
                self.stats["offen"] += 1

            elif status == "bestätigt":
                self.stats["bestätigt"] += 1

            elif status == "vergütet":
                self.stats["vergütet"] += 1
                self.stats["revenue"] += amount

            elif status == "storniert":
                self.stats["storniert"] += 1

        return self.stats
