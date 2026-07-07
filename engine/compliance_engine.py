from engine.google_sheets_live import GoogleSheetsLive


FORBIDDEN_RULES = [

    "wir übernehmen",
    "unabhängig",
    "objektiver vergleich",
    "beste",
    "günstig",
    "profitieren",
    "garantiert",
    "günstig wechseln",
    "kosten senken",
    "schufa-frei",
    "ohne schufa",
    "preisversprechen"

]


class ComplianceEngine:


    def __init__(
        self,
        sheet_id=None,
        credentials=None
    ):

        self.rules = []

        if sheet_id and credentials:

            self.sheets = GoogleSheetsLive(
                sheet_id,
                credentials
            )

            self.load_rules()



    # =========================
    # LOAD RULES
    # =========================

    def load_rules(self):

        self.rules = self.sheets.read_records(
            "affiliate_rules"
        )



    # =========================
    # TEXT CHECK
    # =========================

    def check_forbidden_words(
        self,
        content
    ):

        text = str(content).lower()

        return [

            rule

            for rule in FORBIDDEN_RULES

            if rule in text

        ]



    # =========================
    # PARTNER RULE CHECK
    # =========================

    def check_partner_rules(
        self,
        partner
    ):

        results = []


        for rule in self.rules:

            if rule.get("partner") == partner:

                results.append({

                    "rule_id":
                        rule.get("rule_id"),

                    "type":
                        rule.get("regel_typ"),

                    "regel":
                        rule.get("regel")

                })


        return results



    # =========================
    # FULL AUDIT
    # =========================

    def audit(
        self,
        content,
        partner=None
    ):


        errors = self.check_forbidden_words(
            content
        )


        partner_rules = []


        if partner:

            partner_rules = self.check_partner_rules(
                partner
            )


        return {

            "status":
                "BLOCKED"
                if errors
                else "COMPLIANT",


            "errors":
                errors,


            "partner_rules":
                partner_rules

        }



# =========================
# COMPATIBILITY FUNCTION
# =========================

def check(content):

    text = str(content).lower()

    return [

        rule

        for rule in FORBIDDEN_RULES

        if rule in text

    ]


def audit(content):

    errors = check(content)

    return {

        "status":
            "COMPLIANT"
            if not errors
            else "BLOCKED",

        "errors":
            errors

    }
