class PublishEngine:

    # =========================
    # ROUTING LOGIC (TELEKOM + AFFILIATE)
    # =========================
    def route_product(self, product_id):

        # Telekom Spezial Routing
        if product_id.startswith("TEL_"):
            return {
                "type": "telekom",
                "route": "DIRECT_SHOP",
                "url": "https://free-basics.telekom-profis.de",
                "tracking": "telekom_direct"
            }

        # Check24 / Tarifcheck / Amazon
        if product_id.startswith("CHK"):
            return {
                "type": "check24",
                "route": "affiliate",
                "tracking": "chk24_tracking"
            }

        if product_id.startswith("TC"):
            return {
                "type": "tarifcheck",
                "route": "affiliate",
                "tracking": "tarifcheck_partner_165274"
            }

        if product_id.startswith("AMZ"):
            return {
                "type": "amazon",
                "route": "affiliate",
                "tracking": "amazon_partner"
            }

        return {
            "type": "unknown",
            "route": "safe"
        }

    # =========================
    # COMPLIANCE CHECK
    # =========================
    def compliance_check(self, text):

        forbidden = [
            "garantiert",
            "sicher sparen",
            "beste Anbieter",
            "100% billig"
        ]

        for f in forbidden:
            if f in text:
                return {
                    "status": "BLOCKED",
                    "reason": f
                }

        return {"status": "OK"}

    # =========================
    # FINAL PUBLISH OBJECT
    # =========================
    def publish(self, product_id, content):

        route = self.route_product(product_id)
        check = self.compliance_check(str(content))

        if check["status"] != "OK":
            return {
                "status": "BLOCKED",
                "reason": check["reason"]
            }

        return {
            "product_id": product_id,
            "route": route,
            "content": content,
            "status": "PUBLISHED_READY"
        }
