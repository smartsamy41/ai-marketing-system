from datetime import datetime


class MoneyTracking:

    def __init__(self, sheets=None, bigquery=None):

        self.sheets = sheets
        self.bigquery = bigquery


    # =========================
    # CLICK TRACKING
    # =========================

    def log_click(
        self,
        product,
        category=None,
        partner=None,
        url=None
    ):

        event = {
            "type": "click",
            "product": product,
            "category": category,
            "partner": partner,
            "url": url,
            "timestamp": datetime.utcnow().isoformat()
        }

        self._save(event)

        return {
            "status": "click_saved",
            "event": event
        }


    # =========================
    # CONVERSION TRACKING
    # =========================

    def log_conversion(
        self,
        product,
        value,
        category=None,
        partner=None
    ):

        event = {
            "type": "conversion",
            "product": product,
            "category": category,
            "partner": partner,
            "value": float(value),
            "timestamp": datetime.utcnow().isoformat()
        }

        self._save(event)

        return {
            "status": "conversion_saved",
            "event": event
        }


    # =========================
    # REVENUE
    # =========================

    def calculate_revenue(self, conversions):

        return sum(
            float(item.get("value", 0))
            for item in conversions
        )


    # =========================
    # REPORT
    # =========================

    def category_report(self, events):

        report = {}

        for event in events:

            category = event.get(
                "category",
                "unknown"
            )

            if category not in report:
                report[category] = {
                    "clicks": 0,
                    "conversions": 0,
                    "revenue": 0
                }

            if event["type"] == "click":
                report[category]["clicks"] += 1

            if event["type"] == "conversion":
                report[category]["conversions"] += 1
                report[category]["revenue"] += float(
                    event.get("value", 0)
                )

        return report


    # =========================
    # SAVE LAYER
    # =========================

    def _save(self, event):

        if self.sheets:

            try:
                self.sheets.append(
                    "tracking",
                    event
                )
            except Exception:
                pass


        if self.bigquery:

            try:
                self.bigquery.log(
                    "money_event",
                    event
                )
            except Exception:
                pass
