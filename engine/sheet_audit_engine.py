import os
from datetime import datetime


class SheetAuditEngine:

    def __init__(self):
        self.spreadsheet_id = os.getenv(
            "SPREADSHEET_ID",
            "1p3o008Q57LOP2tEZbvL6OyhTaNrZKKyGZmbpqC0KSKg"
        )
        self.sheet_range = "products!A:Z"

        self.required_columns = [
            "product_id",
            "product_name",
            "source",
            "category",
            "affiliate_url",
            "image_url",
            "landingpage_url",
            "pin_title",
            "pin_description",
            "blog_title",
            "youtube_title",
            "status",
            "seo_title",
            "meta_description",
            "youtube_description",
            "official_direct_link"
        ]

        self.valid_sources = [
            "check24",
            "tarifcheck",
            "amazon",
            "telekom"
        ]

    def load_sheet(self):
        from google.auth import default
        from googleapiclient.discovery import build

        creds, _ = default(scopes=[
            "https://www.googleapis.com/auth/spreadsheets.readonly"
        ])

        service = build("sheets", "v4", credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.sheet_range
        ).execute()

        values = result.get("values", [])

        if not values:
            return [], [], "products sheet leer"

        headers = [h.strip() for h in values[0]]
        rows = values[1:]

        products = []

        for row_values in rows:
            row = {}

            for i, header in enumerate(headers):
                row[header] = row_values[i].strip() if i < len(row_values) else ""

            if row.get("product_id"):
                products.append(row)

        return headers, products, None

    def is_empty(self, value):
        return value is None or str(value).strip() == ""

    def audit_columns(self, headers):
        missing = []

        for col in self.required_columns:
            if col not in headers:
                missing.append(col)

        return {
            "status": "PASS" if not missing else "ERROR",
            "missing_columns": missing
        }

    def audit_counts(self, products):
        counts = {
            "check24": 0,
            "tarifcheck": 0,
            "amazon": 0,
            "telekom": 0,
            "unknown": 0
        }

        for p in products:
            source = p.get("source", "").lower().strip()

            if source in counts:
                counts[source] += 1
            else:
                counts["unknown"] += 1

        expected = {
            "check24": 8,
            "tarifcheck": 9,
            "amazon": 17,
            "telekom": 10
        }

        errors = []

        for source, expected_count in expected.items():
            if counts[source] != expected_count:
                errors.append(
                    f"{source}: expected {expected_count}, found {counts[source]}"
                )

        if counts["unknown"] > 0:
            errors.append(f"unknown source found: {counts['unknown']}")

        return {
            "status": "PASS" if not errors else "ERROR",
            "counts": counts,
            "errors": errors
        }

    def audit_duplicates(self, products):
        seen = set()
        duplicates = []

        for p in products:
            product_id = p.get("product_id", "").strip()

            if product_id in seen:
                duplicates.append(product_id)
            else:
                seen.add(product_id)

        return {
            "status": "PASS" if not duplicates else "ERROR",
            "duplicates": duplicates
        }

    def audit_required_fields(self, products):
        results = []
        total_errors = 0
        total_warnings = 0

        for p in products:
            product_id = p.get("product_id", "")
            source = p.get("source", "").lower().strip()

            errors = []
            warnings = []

            basic_required = [
                "product_id",
                "product_name",
                "source",
                "category",
                "status",
                "seo_title",
                "meta_description",
                "blog_title",
                "youtube_title",
                "pin_title"
            ]

            for field in basic_required:
                if self.is_empty(p.get(field)):
                    errors.append(f"missing {field}")

            if source not in self.valid_sources:
                errors.append(f"invalid source: {source}")

            if source != "telekom":
                if self.is_empty(p.get("affiliate_url")) and self.is_empty(p.get("official_direct_link")):
                    errors.append("missing affiliate_url or official_direct_link")

                if self.is_empty(p.get("landingpage_url")):
                    errors.append("missing landingpage_url")

            if source == "amazon":
                if self.is_empty(p.get("image_url")):
                    errors.append("amazon image_url missing")

                affiliate = p.get("affiliate_url", "") + p.get("official_direct_link", "")

                if "freebasics-21" not in affiliate:
                    warnings.append("amazon tracking id freebasics-21 not found")

            if source == "tarifcheck":
                affiliate = p.get("affiliate_url", "") + p.get("official_direct_link", "")

                if "partner_id=165274" not in affiliate:
                    errors.append("tarifcheck partner_id=165274 missing")

            if source == "telekom":
                link = p.get("affiliate_url", "") or p.get("official_direct_link", "") or p.get("landingpage_url", "")

                if "free-basics.telekom-profis.de" not in link:
                    errors.append("telekom shop link missing")

            status = "PASS"
            if warnings:
                status = "WARNING"
            if errors:
                status = "ERROR"

            total_errors += len(errors)
            total_warnings += len(warnings)

            results.append({
                "product_id": product_id,
                "product_name": p.get("product_name", ""),
                "source": source,
                "status": status,
                "errors": errors,
                "warnings": warnings
            })

        return {
            "status": "PASS" if total_errors == 0 else "ERROR",
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "results": results
        }

    def run_audit(self):
        headers, products, load_error = self.load_sheet()

        if load_error:
            return {
                "status": "ERROR",
                "stage": "LOAD_SHEET",
                "error": load_error,
                "checked_at": datetime.utcnow().isoformat()
            }

        column_audit = self.audit_columns(headers)
        count_audit = self.audit_counts(products)
        duplicate_audit = self.audit_duplicates(products)
        field_audit = self.audit_required_fields(products)

        errors = []

        for block in [column_audit, count_audit, duplicate_audit, field_audit]:
            if block.get("status") == "ERROR":
                errors.append(block)

        final_status = "PASS" if not errors else "ERROR"

        return {
            "status": final_status,
            "audit": "RC1.1_SHEET_AUDIT",
            "checked_at": datetime.utcnow().isoformat(),
            "product_count": len(products),
            "columns": column_audit,
            "counts": count_audit,
            "duplicates": duplicate_audit,
            "required_fields": field_audit,
            "ready_for_rc1_2": final_status == "PASS"
        }
