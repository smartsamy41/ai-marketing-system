from typing import Any

from engine.google_sheets_live import GoogleSheetsLive


FORBIDDEN_RULES = [
    "wir übernehmen",
    "unabhängig",
    "objektiver vergleich",
    "beste",
    "besten",
    "günstig",
    "profitieren",
    "garantiert",
    "günstig wechseln",
    "kosten senken",
    "schufa-frei",
    "ohne schufa",
    "preisversprechen",
]


class ComplianceEngine:

    def __init__(
        self,
        sheet_id: str | None = None,
        credentials: str | None = None
    ):

        self.sheets = GoogleSheetsLive(
            spreadsheet_id=sheet_id,
            credentials_json=credentials
        )

        self.rules: list[dict[str, Any]] = []

        self.load_rules()


    # ========================================================
    # NORMALIZATION
    # ========================================================

    @staticmethod
    def _normalize(value: Any) -> str:

        return str(
            value or ""
        ).strip().lower()


    # ========================================================
    # LOAD RULES
    # ========================================================

    def load_rules(self) -> None:

        self.rules = self.sheets.read_records(
            "affiliate_rules",
            "A:ZZ"
        )


    # ========================================================
    # TEXT CHECK
    # ========================================================

    def check_forbidden_words(
        self,
        content: Any
    ) -> list[str]:

        text = self._normalize(
            content
        )

        return [
            rule
            for rule in FORBIDDEN_RULES
            if rule in text
        ]


    # ========================================================
    # PARTNER RULE CHECK
    # ========================================================

    def check_partner_rules(
        self,
        partner: str | None
    ) -> list[dict[str, Any]]:

        normalized_partner = self._normalize(
            partner
        )

        if not normalized_partner:
            return []

        results = []

        for rule in self.rules:

            rule_partner = self._normalize(
                rule.get("partner")
            )

            if rule_partner != normalized_partner:
                continue

            results.append({
                "rule_id": rule.get("rule_id"),
                "partner": rule.get("partner"),
                "bereich": rule.get("bereich"),
                "type": rule.get("regel_typ"),
                "regel": rule.get("regel"),
                "aktion": rule.get("aktion"),
                "pflicht": rule.get("pflicht"),
                "verbot": rule.get("verbot"),
                "quelle": rule.get("quelle"),
                "status": rule.get("status"),
            })

        return results


    # ========================================================
    # FULL AUDIT
    # ========================================================

    def audit(
        self,
        content: Any,
        partner: str | None = None
    ) -> dict[str, Any]:

        errors = self.check_forbidden_words(
            content
        )

        partner_rules = self.check_partner_rules(
            partner
        )

        return {
            "status": (
                "BLOCKED"
                if errors
                else "COMPLIANT"
            ),
            "errors": errors,
            "partner_rules": partner_rules,
        }


# ============================================================
# COMPATIBILITY FUNCTIONS
# ============================================================

def check(content: Any) -> list[str]:

    text = str(
        content or ""
    ).strip().lower()

    return [
        rule
        for rule in FORBIDDEN_RULES
        if rule in text
    ]


def audit(content: Any) -> dict[str, Any]:

    errors = check(
        content
    )

    return {
        "status": (
            "COMPLIANT"
            if not errors
            else "BLOCKED"
        ),
        "errors": errors,
    }
