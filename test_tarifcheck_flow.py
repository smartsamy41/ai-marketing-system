from engine.commission_engine import CommissionEngine
from engine.revenue_engine import RevenueEngine


sheet_id = open(
    "/tmp/fb_secrets/sheet_id.txt"
).read().strip()

creds = open(
    "/tmp/fb_secrets/service_account.json"
).read().strip()


commission = CommissionEngine(
    sheet_id,
    creds
)

revenue = RevenueEngine()


# =========================
# SIMULIERTER TARIFCHECK SALE
# =========================

sale = {

    "partner": "Tarifcheck",

    "product_id": "TC_003",

    "status": "vergütet",

    # Beispiel aus API amount_net
    "amount_net": 145.66
}


print("\nSALE:")
print(sale)


# =========================
# COMMISSION
# =========================

commission_data = commission.get_commission(
    sale["product_id"]
)


print("\nCOMMISSION:")
print(commission_data)


# =========================
# REVENUE BERECHNUNG
# =========================

value = commission.calculate_sale_value(
    sale["product_id"],
    sale["amount_net"]
)


print("\nCALCULATED VALUE:")
print(value)


if sale["status"] == "vergütet":

    revenue.track_conversion(
        value
    )


print("\nREVENUE:")
print(
    revenue.stats()
)
