import json


FILE = "audits/live_geo_audit_report.json"


with open(
    FILE,
    encoding="utf-8"
) as f:
    data = json.load(f)


print("=" * 60)
print("GEO COMPLIANCE WARNINGS")
print("=" * 60)


count = 0


for item in data["results"]:

    if item["forbidden_terms"]:

        count += 1

        print()
        print("PRODUCT:", item["product_id"])
        print("URL:", item["url"])
        print("TERMS:", item["forbidden_terms"])
        print("STATUS:", item["status"])


print()
print("=" * 60)
print("WARNINGS:", count)
print("=" * 60)
