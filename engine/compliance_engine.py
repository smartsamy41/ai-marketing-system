from datetime import datetime

FORBIDDEN_TERMS = [
    "ohne schufa",
    "schufa-frei",
    "tüv-siegel",
    "tuv-siegel",
    "garantiert",
    "preisversprechen",
    "unabhängig",
    "objektiver vergleich",
    "beste",
    "günstig",
    "sparen"
]

BRAND_MAP = {
    "energie": "CHECK24",
    "finanzen": "TARIFCHECK",
    "tech": "AMAZON",
    "telekom": "TELEKOM"
}


# =========================
# CORE CHECK
# =========================
def check_content(content: str):

    text = str(content or "").lower()

    found_forbidden = [
        t for t in FORBIDDEN_TERMS if t in text
    ]

    return {
        "blocked": len(found_forbidden) > 0,
        "violations": found_forbidden
    }


# =========================
# STRICT VALIDATION (NEW)
# =========================
def validate_landingpage(content: str, category: str):

    text = str(content or "").lower()
    category = str(category or "").lower()

    errors = []

    # affiliate disclosure mandatory
    if "werbung" not in text and "anzeige" not in text:
        errors.append("missing_affiliate_label")

    # partner isolation rule
    expected = BRAND_MAP.get(category)

    if expected and expected.lower() not in text:
        errors.append("missing_partner_reference")

    # forbidden terms
    forbidden = check_content(content)
    if forbidden["blocked"]:
        errors.append("forbidden_terms_detected")

    return {
        "status": "BLOCKED" if errors else "OK",
        "errors": errors,
        "timestamp": str(datetime.now())
    }


# =========================
# COMPLIANCE ENGINE CLASS
# =========================
class ComplianceEngine:

    def audit(self, content, category):
        return validate_landingpage(content, category)

    def is_allowed(self, content, category):
        result = self.audit(content, category)
        return result["status"] == "OK"
