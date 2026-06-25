from engine.landingpage_engine_v2 import LandingpageQualityFixV1
from engine.tracking_engine import tracking
from engine.api_connector import APIConnector
from engine.profit_engine import ProfitEngine
from engine.partner_commission_mapper import PartnerCommissionMapper
from engine.compliance_engine import ComplianceEngine


class OrchestratorCleanMaster:

    def __init__(self):

        self.api = APIConnector()
        self.profit_engine = ProfitEngine()
        self.commission_mapper = PartnerCommissionMapper()
        self.compliance_engine = ComplianceEngine()

    # =========================
    # SINGLE PRODUCT FLOW
    # =========================
    def run(self, product_id):

        try:

            # -------------------------
            # LANDINGPAGE (FIXED)
            # -------------------------
            landingpage = LandingpageQualityFixV1()
            lp = landingpage.build(product_id)

            # -------------------------
            # TRACKING
            # -------------------------
            track = tracking.track(product_id)

            # -------------------------
            # SALES (SAFE)
            # -------------------------
            sales_raw = self.api.send_sales_lead(product_id)

            if not isinstance(sales_raw, dict):
                sales_raw = {
                    "status": "ERROR",
                    "code": 0,
                    "data": [],
                    "error": "Invalid response"
                }

            sales = {
                "type": "sales",
                "status": sales_raw.get("status"),
                "code": sales_raw.get("code", 0),
                "data": sales_raw.get("data", []),
                "error": sales_raw.get("error")
            }

            # -------------------------
            # PROFIT
            # -------------------------
            profit = self.profit_engine.process_product(product_id)

            # -------------------------
            # COMMISSION
            # -------------------------
            commission = self.commission_mapper.get(product_id)

            # -------------------------
            # COMPLIANCE
            # -------------------------
            compliance = self.compliance_engine.audit(
                content=str(profit),
                product={"source": "tarifcheck"}
            )

            # -------------------------
            # FINAL OUTPUT
            # -------------------------
            return {
                "product_id": product_id,
                "landingpage": lp,
                "tracking": track,
                "sales": sales,
                "profit": profit,
                "commission": commission,
                "compliance": compliance,
                "status": "OK"
            }

        except Exception as e:

            return {
                "product_id": product_id,
                "status": "FAILED_SAFE",
                "error": str(e)
            }

    # =========================
    # BATCH RUN
    # =========================
    def run_all(self, products):

        results = []

        for p in products:
            results.append(self.run(p))

        return results
