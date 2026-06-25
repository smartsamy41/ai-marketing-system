from datetime import datetime


class ProfitEngine:

    def __init__(self, sales_engine, compliance_engine, commission_engine):

        self.sales_engine = sales_engine
        self.compliance_engine = compliance_engine
        self.commission_engine = commission_engine

    # =========================
    # MAP PRODUCT → COMMISSION
    # =========================
    def get_commission_value(self, product_id):

        result = self.commission_engine.get_commission(product_id)

        if result.get("status") != "OK":
            return 0.0

        return float(result.get("commission_value", 0) or 0)

    # =========================
    # PROCESS SINGLE PRODUCT PROFIT
    # =========================
    def process_product(self, product_id):

        # 1. GET SALES DATA
        sales = self.sales_engine.send_sales_lead(product_id)

        leads = sales.get("data", [])

        total_revenue = 0.0
        total_profit = 0.0

        processed_leads = []

        for lead in leads:

            status = lead.get("status")
            amount = float(lead.get("amount_net", 0) or 0)

            # 2. ONLY VALID LEADS COUNT
            if status in ["vergütet", "bestätigt"]:

                commission = self.get_commission_value(product_id)

                profit = commission

                total_revenue += amount
                total_profit += profit

                processed_leads.append({
                    "lead_id": lead.get("id"),
                    "status": status,
                    "revenue": amount,
                    "commission": commission,
                    "profit": profit
                })

        return {
            "product_id": product_id,
            "total_revenue": round(total_revenue, 2),
            "total_profit": round(total_profit, 2),
            "leads": processed_leads,
            "timestamp": str(datetime.now())
        }

    # =========================
    # RUN FULL PORTFOLIO
    # =========================
    def run_all(self, product_ids):

        results = []

        for pid in product_ids:
            results.append(self.process_product(pid))

        # TOTAL SYSTEM PROFIT
        total = sum(r["total_profit"] for r in results)

        return {
            "status": "OK",
            "total_profit": round(total, 2),
            "products": results,
            "timestamp": str(datetime.now())
        }
