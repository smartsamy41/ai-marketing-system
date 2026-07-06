from datetime import datetime


class MoneyTracking:
    """
    Production Money Tracking Layer

    Erfasst:
    - Klicks
    - Conversions
    - Revenue
    - Partner
    - Kategorien

    Optional:
    - Google Sheets
    - BigQuery
    """

    def __init__(self, sheets=None, bigquery=None):

        self.sheets = sheets
        self.bigquery = bigquery

        self.events = []


    # =========================
    # CLICK EVENT
    # =========================

    def log_click(
        self,
        product,
        category=None,
        partner=None,
        url=None
    ):

        event = {
            "event": "click",
            "product": product,
            "category": category,
            "partner": partner,
            "url": url,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.events.append(event)

        self._store(event)

        return {
            "status": "click_saved",
            "event": event
        }


    # =========================
    # CONVERSION EVENT
    # =========================

    def log_conversion(
        self,
        product,
        value,
        category=None,
        partner=None
    ):

        event = {
            "event": "conversion",
            "product": product,
            "category": category,
            "partner": partner,
            "value": float(value),
            "timestamp": datetime.utcnow().isoformat()
        }

        self.events.append(event)

        self._store(event)

        return {
            "status": "conversion_saved",
            "event": event
        }


    # =========================
    # TOTAL REVENUE
    # =========================

    def revenue(self):

        total = 0

        for event in self.events:

            if event.get("event") == "conversion":

                total += float(
                    event.get("value", 0)
                )

        return total


    # =========================
    # CATEGORY REPORT
    # =========================

    def report(self):

        result = {}

        for event in self.events:

            category = event.get(
                "category",
                "unknown"
            )

            if category not in result:

                result[category] = {
                    "clicks": 0,
                    "conversions": 0,
                    "revenue": 0
                }


            if event["event"] == "click":

                result[category]["clicks"] += 1


            if event["event"] == "conversion":

                result[category]["conversions"] += 1

                result[category]["revenue"] += float(
                    event.get("value", 0)
                )


        return result


    # =========================
    # STORAGE CONNECTION
    # =========================

    def _store(self, event):

        # Google Sheets

        if self.sheets:

            try:
                self.sheets.append(
                    "tracking",
                    event
                )

            except Exception:
                pass


        # BigQuery

        if self.bigquery:

            try:

                self.bigquery.log(
                    "money_tracking",
                    event
                )

            except Exception:
                pass
