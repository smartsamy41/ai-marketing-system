from datetime import datetime
import traceback

from engine.data_layer_engine import load_products, load_assets
from engine.orchestrator_engine import run_orchestrator
from engine.routing_engine import route_product

from engine.content_engine import build_content
from engine.monetization_engine import inject_monetization
from engine.compliance_engine import apply_compliance, audit_content

from engine.landingpage_v4_engine import build_landingpage_v4
from engine.tracking_engine import track_event
from engine.learning_engine import learn_from_results
from engine.output_layer import route_output

from engine.youtube_engine_v1 import build_youtube_entry
from engine.dashboard_engine import build_dashboard

from engine.cleanup_engine import run_cleanup_system


def _now():
    return str(datetime.now())


def run_master_engine():

    try:

        products = load_products() or []
        assets = load_assets() or {}

        if not products:
            return {
                "status": "NO_PRODUCTS",
                "executed": 0,
                "results": [],
                "time": _now()
            }

        # CLEANUP LAYER (PRODUCTION SAFE)
        run_cleanup_system({
            "landingpages": [],
            "blog_posts": []
        })

        plan = run_orchestrator(products) or {"schedule": {}}

        results = []

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
                        product=product
                    )

                    if route.get("landingpage_required"):

                        landing = build_landingpage_v4(
                            product=product,
                            assets=assets
                        )

                        audit = audit_content(
                            landing.get("lp_html", ""),
                            product=product
                        )

                    else:
                        landing = {
                            "status": "DIRECT",
                            "url": route.get("target_url")
                        }
                        audit = {"status": "SKIPPED"}

                    youtube = build_youtube_entry(product, route)

                    output = route_output(product)
                    tracking = track_event(product, output)
                    learning = learn_from_results(product, tracking)

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
                        "status": "OK"
                    })

                except Exception as e:

                    results.append({
                        "product_id": item.get("product_id"),
                        "status": "ERROR",
                        "error": str(e),
                        "trace": traceback.format_exc()
                    })

        dashboard = build_dashboard(products, {}, assets, {})

        return {
            "status": "SUCCESS",
            "mode": "PRODUCTION_V1",
            "executed": len(results),
            "dashboard": dashboard,
            "results": results,
            "sample": results[0] if results else None,
            "time": _now()
        }

    except Exception as e:

        return {
            "status": "FATAL_ERROR",
            "error": str(e),
            "trace": traceback.format_exc(),
            "time": _now()
        }
