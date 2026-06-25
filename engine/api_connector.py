def send_sales_lead(self, product_id):

    url = os.getenv("TARIFCHECK_API_URL")
    username = os.getenv("TARIFCHECK_USERNAME")
    password = os.getenv("TARIFCHECK_PASSWORD")

    if not url or not username or not password:
        return {
            "type": "sales",
            "status": "SKIPPED",
            "error": "Missing ENV credentials"
        }

    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(username, password),
            timeout=20
        )

        # 🟢 CLEAN JSON ONLY ONCE
        data = response.json()

        return {
            "type": "sales",
            "status": "OK",
            "code": response.status_code,
            "data": data.get("data", [])
        }

    except Exception as e:
        return {
            "type": "sales",
            "status": "ERROR",
            "error": str(e)
        }
