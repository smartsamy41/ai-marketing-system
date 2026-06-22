from datetime import datetime
import traceback


# ENGINE IMPORTS
from engine.data_layer_engine import (
    load_products,
    load_assets,
    load_commissions,
    load_partner_rules
)

from engine.decision_engine import evaluate_products
from engine.content_engine import build_content
from engine.orchestrator_engine import run_orchestrator
from engine.routing_engine import route_product

from engine.monetization_engine import inject_monetization
from engine.compliance_engine import apply_compliance, audit_content

from engine.landingpage_v4_engine import build_landingpage_v4
from engine.auto_fix_engine import auto_fix_posts

from engine.tracking_engine import track_event
from engine.learning_engine import learn_from_results

from engine.output_layer import route_output as send_output

from engine.dashboard_engine import build_dashboard

from engine.youtube_engine_v1 import build_youtube_entry


# =========================
# TIME
# =========================
def _now():
    return str(datetime.now())


# =========================
# MASTER ENGINE V4
# =========================
def run_master_engine():

    try:
        # -------------------------
        # LOAD SYSTEM STATE
        # -------------------------
        products = load_products() or []
        assets = load_assets() or {}
        commissions = load_commissions() or {}
        partner_rules = load_partner_rules() or {}

        if len(products) == 0:
            return {
                "status": "ERROR",
                "message": "NO_PRODUCTS_FOUND",
                "executed": 0,
                "results": [],
                "time": _now()
            }

        # -------------------------
        # PRODUCT SCORING
        # -------------------------
        products = evaluate_products(products, commissions) or products

        # -------------------------
        # DASHBOARD BUILD
        # -------------------------
        dashboard = build_dashboard(
            products=products,
            commissions=commissions,
            assets=assets,
            rules=partner_rules
        )

        # -------------------------
        # ORCHESTRATION PLAN
        # -------------------------
        plan = run_orchestrator(products) or {"schedule": {}}

        final_results = []

        # -------------------------
        # EXECUTION LOOP
        # -------------------------
        for slot, items in plan.get("schedule", {}).items():

            for item in items:

                try:
                    product_id = item.get("product_id")

                    product = next(
                        (p for p in products if p.get("product_id") == product_id),
                        None
                    )

                    if not product:
                        continue

                    # -------------------------
                    # ROUTING
                    # -------------------------
                    route = route_product(product)

                    # -------------------------
                    # CONTENT GENERATION
                    # -------------------------
                    content = build_content(product) or {}

                    # -------------------------
                    # MONETIZATION
                    # -------------------------
                    monetized_content = inject_monetization(
                        content=content,
                        product=product,
                        assets=assets
                    ) or {}

                    # -------------------------
                    # COMPLIANCE CHECK
                    # -------------------------
                    compliance = apply_compliance(
                        content=monetized_content.get("text", ""),
                        product=product,
                        rules=partner_rules
                    )

                    # -------------------------
                    # LANDINGPAGE LOGIC
                    # -------------------------
                    if route.get("landingpage_required"):

                        landingpage = build_landingpage_v4(
                            product=product,
                            assets=assets,
                            commissions=commissions,
                            rules=partner_rules
                        )

                        landingpage_audit = audit_content(
                            content=landingpage.get("lp_html", ""),
                            product=product,
                            rules=partner_rules
                        )

                    else:
                        landingpage = {
                            "status": "SKIPPED_DIRECT_TO_SHOP",
                            "url_path": route.get("target_url"),
                            "affiliate_url": route.get("target_url"),
                            "lp_html": ""
                        }

                        landingpage_audit = {"status": "SKIPPED"}

                    # -------------------------
                    # AUTO FIX
                    # -------------------------
                    fixed = auto_fix_posts([{
                        "post_id": product_id,
                        "content": monetized_content.get("text", ""),
                        "source": product.get("source"),
                        "links": [route.get("target_url")]
                    }])

                    # -------------------------
                    # YOUTUBE ENTRY
                    # -------------------------
                    youtube = build_youtube_entry(product, route)

                    # -------------------------
                    # OUTPUT + TRACKING
                    # -------------------------
                    output = send_output(product)
                    tracking = track_event(product, output)
                    learning = learn_from_results(product, tracking)

                    # -------------------------
                    # RESULT
                    # -------------------------
                    final_results.append({
                        "product_id": product_id,
                        "slot": slot,
                        "route": route,
                        "content": content,
                        "monetized_content": monetized_content,
                        "compliance": compliance,
                        "landingpage": landingpage,
                        "landingpage_audit": landingpage_audit,
                        "youtube": youtube,
                        "tracking": tracking,
                        "learning": learning,
                        "output": output,
                        "status": "OK"
                    })

                except Exception as e:

                    final_results.append({
                        "product_id": item.get("product_id"),
                        "status": "ERROR",
                        "error": str(e),
                        "traceback": traceback.format_exc()
                    })

        return {
            "status": "SUCCESS",
            "mode": "MASTER_ENGINE_V4_PRODUCTION",
            "executed": len(final_results),
            "dashboard": dashboard,
            "results": final_results,
            "sample": final_results[0] if final_results else None,
            "time": _now()
        }

    except Exception as e:

        return {
            "status": "FATAL_ERROR",
            "message": str(e),
            "traceback": traceback.format_exc(),
            "executed": 0,
            "results": [],
            "time": _now()
        }
