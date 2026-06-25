from engine.tarifcheck_sales_engine import TarifcheckSalesEngine

@app.get("/test-sales")
def test_sales():

    engine = TarifcheckSalesEngine()
    result = engine.fetch_leads()

    return {
        "status": "PHASE_2_SALES_TEST",
        "result": result
    }
