from engine.api_connector import APIConnector
from compliance_engine import ComplianceEngine
from profit_engine import ProfitEngine


class FlowController:

    def __init__(self):

        self.api = APIConnector()
        self.compliance = ComplianceEngine()

        self.profit = ProfitEngine(
            sales_engine=self.api,
            compliance_engine=self.compliance,
            commission_engine=self.compliance
        )

    # =========================
    # SINGLE PRODUCT FLOW
    # =========================
    def run_product(self, product_id):

        # 1. SALES + PROFIT
        profit_data = self.profit.process_product(product_id)

        # 2. COMPLIANCE CHECK
        compliance = self.compliance.audit(
            content=str(profit_data),
            product={"source": "tarifcheck"}
        )

        # 3. OUTPUT DATA (NO NEW ENGINE, ONLY STRUCTURE)
        return {
            "product_id": product_id,
            "profit": profit_data,
            "compliance": compliance
        }

    # =========================
    # FULL SYSTEM RUN
    # =========================
    def run_all(self, product_ids):

        results = []

        for pid in product_ids:
            results.append(self.run_product(pid))

        total_profit = sum(
            r["profit"]["total_profit"]
            for r in results
        )

        return {
            "status": "OK",
            "total_profit": round(total_profit, 2),
            "results": results
        }
