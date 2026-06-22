from datetime import datetime
import traceback

from engine.data_layer_engine import (
    load_products,
    load_assets,
    load_commissions,
    load_partner_rules
)

from engine.decision_engine import evaluate_products
from engine.orchestrator_engine import run_orchestrator
from engine.routing_engine import route_product

from engine.content_engine import build_content
from engine.monetization_engine import inject_monetization
from engine.compliance_engine import apply_compliance, audit_content

from engine.landingpage_v4_engine import build_landingpage_v4
from engine.auto_fix_engine import auto_fix_posts

from engine.tracking_engine import track_event
from engine.learning_engine import learn_from_results

from engine.output_layer import route_output

from engine.youtube_engine_v1 import build_youtube_entry

from engine.cleanup_engine import run_cleanup_system

from engine.traffic_loop_engine import run_traffic_loop

from engine.real_traffic_connector import run_real_traffic_connector

from engine.real_data_connector_v2 import run_real_data_connector_v2

from engine.money_dashboard_v1 import run_money_dashboard


def _now():
    return str(datetime.now())


def run_master_engine():

    try:

        # =========================
        # LOAD SYSTEM DATA
        # =========================

        products = load_products() or []
        assets = load_assets() or {}
        commissions = load_commissions() or {}
        partner_rules = load_partner_rules() or {}

        if not products:
            return {
                "status": "NO_PRODUCTS",
                "executed": 0,
                "results": [],
                "time": _now()
            }

        # =========================
        # CLEANUP LAYER
        # =========================

        run_cleanup_system({
            "landingpages": [],
            "blog_posts": []
        })

        # =========================
        # PRODUCT SCORING
        # =========================

        products = evaluate_products(products, commissions) or products

        # =========================
        # ORCHESTRATION
        # =========================

        plan = run_orchestrator(products) or {"schedule": {}}

        results = []

        traffic_input = []

        # =========================
        # MAIN EXECUTION LOOP
        # =========================

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

                    route = route_product(product)

                    content = build_content(product) or {}

                    monetized = inject_monetization(
                        content=content,
                        product=product,
                        assets=assets
                    ) or {}

                    compliance = apply_compliance(
                        content=monetized.get("text", ""),
                        product=product,
                        rules=partner_rules
                    )

                    if route.get("landingpage_required"):

                        landing = build_landingpage_v4(
                            product=product,
                            assets=assets,
                            commissions=commissions,
                            rules=partner_rules
                        )

                        audit = audit_content(
                            landing.get("lp_html", ""),
                            product=product,
                            rules=partner_rules
                        )

                    else:
                        landing = {
                            "status": "DIRECT",
                            "url": route.get("target_url")
                        }
                        audit = {"status": "SKIPPED"}

                    auto_fix_posts([{
                        "post_id": product_id,
                        "content": monetized.get("text", ""),
                        "source": product.get("source"),
                        "links": [route.get("target_url")]
                    }])

                    youtube = build_youtube_entry(product, route)

                    output = route_output(product)
                    tracking = track_event(product, output)
                    learning = learn_from_results(product, tracking)

                    traffic_input.append({
                        "product_id": product_id,
                        "source": product.get("source", "unknown"),
                        "clicks": tracking.get("clicks", 0),
                        "revenue": tracking.get("revenue", 0)
                    })

                    results.append({
                        "product_id": product_id,
                        "slot": slot,
                        "route": route,
                        "content": content,
                        "monetized": monetized,
                        "compliance": compliance,
                        "landingpage": landing,
                        "audit": audit,
                        "youtube": youtube,
                        "tracking": tracking,
                        "learning": learning,
                        "output": output,
                        "status": "OK"
                    })

                except Exception as e:

                    results.append({
                        "product_id": item.get("product_id"),
                        "status": "ERROR",
                        "error": str(e),
                        "trace": traceback.format_exc()
                    })

        # =========================
        # SYSTEM LAYERS OUTPUT
        # =========================

        dashboard = run_money_dashboard(traffic_input)

        traffic = run_traffic_loop(traffic_input)

        real_traffic = run_real_traffic_connector(products)

        real_data = run_real_data_connector_v2([], [])

        # =========================
        # FINAL OUTPUT
        # =========================

        return {
            "status": "SUCCESS",
            "mode": "MASTER_ENGINE_V7_FULL_INTEGRATED",
            "executed": len(results),
            "dashboard": dashboard,
            "traffic": traffic,
            "real_traffic": real_traffic,
            "real_data": real_data,
            "results": results,
            "sample": results[0] if results else None,
            "time": _now()
        }

    except Exception as e:

        return {
            "status": "FATAL_ERROR",
            "error": str(e),
            "trace": traceback.format_exc(),
            "executed": 0,
            "results": [],
            "time": _now()
        }
