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


BRAND_TERMS = [
    "check24-strompreise",
    "check24-strom",
    "check24-gas",
    "tarifcheck24",
    "tarifcheck-24"
]


def _text(value):
    return str(value or "").lower()


def check_forbidden_terms(content):
    text = _text(content)
    found = []

    for term in FORBIDDEN_TERMS + BRAND_TERMS:
        if term in text:
            found.append(term)

    return found


def check_required_notices(content, source):
    text = _text(content)
    source = _text(source)

    errors = []

    if "werbung" not in text and "anzeige" not in text:
        errors.append("affiliate_notice_missing")

    if "tarifcheck" in source:
        if "tippgeber" not in text:
            errors.append("tippgeber_notice_missing")

        if "powered by tarifcheck24 gmbh" not in text:
            errors.append("tarifcheck_powered_by_missing")

        if "zollstr" not in text and "zollstraße" not in text:
            errors.append("tarifcheck_impressum_missing")

    return errors


def build_compliance_notice(product):
    source = _text(product.get("source"))

    if "tarifcheck" in source:
        return (
            "⚠️ Werbung / Anzeige. Free Basics ist Tippgeber und kein "
            "Versicherungsvermittler. Alle Vergleiche powered by "
            "TARIFCHECK24 GmbH, Zollstr. 11b, 21465 Wentorf bei Hamburg, "
            "Tel. 040 - 73098288, Fax 040 - 73098289, "
            "E-Mail: info@tarifcheck.de."
        )

    return (
        "⚠️ Werbung / Anzeige. Diese Seite enthält Affiliate-Links. "
        "Für verifizierte Leads oder Sales kann Free Basics eine Provision erhalten."
    )


def audit_content(content, product=None, rules=None):
    product = product if isinstance(product, dict) else {}
    source = product.get("source")

    errors = []
    warnings = []

    forbidden = check_forbidden_terms(content)
    if forbidden:
        errors.append({
            "type": "forbidden_terms_found",
            "terms": forbidden
        })

    notice_errors = check_required_notices(content, source)
    errors.extend(notice_errors)

    score = 100
    score -= len(errors) * 20
    score -= len(warnings) * 5

    if score < 0:
        score = 0

    status = "COMPLIANT" if not errors else "BLOCKED"

    return {
        "status": status,
        "score": score,
        "errors": errors,
        "warnings": warnings,
        "timestamp": str(datetime.now())
    }


def apply_compliance(content, product=None, rules=None):
    product = product if isinstance(product, dict) else {}

    notice = build_compliance_notice(product)

    safe_content = str(content or "")

    if "werbung" not in safe_content.lower() and "anzeige" not in safe_content.lower():
        safe_content = safe_content + "\n\n" + notice

    audit = audit_content(
        content=safe_content,
        product=product,
        rules=rules
    )

    return {
        "status": audit.get("status"),
        "content": safe_content,
        "audit": audit,
        "timestamp": str(datetime.now())
    }


class ComplianceEngine:
    def __init__(self):
        print("🟢 ComplianceEngine loaded")

    def audit(self, content, product=None, rules=None):
        return audit_content(content, product, rules)

    def apply(self, content, product=None, rules=None):
        return apply_compliance(content, product, rules)
