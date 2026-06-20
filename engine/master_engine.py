from datetime import datetime
import traceback


def run_master_engine():
    try:
        from engine.data_layer_engine import (
            load_products,
            load_assets,
            load_commissions,
            load_partner_rules
        )
        from engine.decision_engine import evaluate_products
        from engine.content_engine import build_content
        from engine.auto_fix_engine import auto_fix_posts
        from engine.orchestrator_engine import run_orchestrator
        from engine.output_layer import route_output as send_output
        from engine.tracking_engine import track_event
        from engine.learning_engine import learn_from_results
        from engine.monetization_engine import inject_monetization
        from engine.compliance_engine import apply_compliance, audit_content
        from engine.dashboard_engine import build_dashboard
        from engine.landingpage_v4_engine import build_landingpage_v4
        from engine.routing_engine import route_product

        products = load_products() or []
        assets = load_assets() or {}
        commissions = load_commissions() or {}
        partner_rules = load_partner_rules() or {}

        if not products:
            return {
                "status": "error",
                "message": "NO_PRODUCTS_FOUND",
                "mode": "MASTER_ENGINE_PRODUCTS_EMPTY",
                "executed": 0,
                "dashboard": {},
                "results": [],
                "sample_product": None,
                "time": str(datetime.now())
            }

        products = evaluate_products(products, commissions) or products

        dashboard = build_dashboard(
            products=products,
            commissions=commissions,
            assets=assets,
            rules=partner_rules
        )

        plan = run_orchestrator(products) or {"schedule": {}}
        final_results = []

        for slot, items in plan.get("schedule", {}).items():
            if not items:
                continue

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

                    monetized_content = inject_monetization(
                        content=content,
                        product=product,
                        assets=assets
                    ) or {}

                    compliance = apply_compliance(
                        content=monetized_content.get("text", ""),
                        product=product,
                        rules=partner_rules
                    )

                    monetized_content["text"] = compliance.get(
                        "content",
                        monetized_content.get("text", "")
                    )
                    monetized_content["compliance_audit"] = compliance.get("audit")

                    landingpage = None
                    landingpage_audit = None

                    if route.get("landingpage_required") is True:
                        landingpage = build_landingpage_v4(
                            product=product,
                            assets=assets,
                            commissions=commissions,
                            rules=partner_rules
                        ) or {}

                        landingpage_audit = audit_content(
                            content=landingpage.get("lp_html", ""),
                            product=product,
                            rules=partner_rules
                        )
                    else:
                        landingpage = {
                            "status": "SKIPPED_DIRECT_TO_SHOP",
                            "product_id": product_id,
                            "source": product.get("source"),
                            "url_path": route.get("target_url"),
                            "full_url": route.get("target_url"),
                            "affiliate_url": route.get("target_url"),
                            "lp_html": "",
                            "lp_seo_title": "",
                            "lp_meta_description": "",
                            "lp_faq": "",
                            "lp_cta": "Zum Shop",
                            "lp_content": "",
                            "timestamp": str(datetime.now())
                        }

                        landingpage_audit = {
                            "status": "SKIPPED",
                            "reason": "DIRECT_TO_SHOP_NO_LANDINGPAGE",
                            "score": 100
                        }

                    auto_fix_result = auto_fix_posts([{
                        "post_id": product_id,
                        "content": monetized_content.get("text", ""),
                        "source": product.get("source"),
                        "links": [
                            route.get("target_url")
                        ]
                    }])

                    if isinstance(auto_fix_result, list) and auto_fix_result:
                        fixed_content = auto_fix_result[0]
                    else:
                        fixed_content = auto_fix_result

                    routing = {
                        "channel": route.get("channel"),
                        "product_id": product_id,
                        "slot": slot,
                        "target_url": route.get("target_url"),
                        "landingpage_required": route.get("landingpage_required"),
                        "route_type": route.get("route_type")
                    }

                    output = send_output(product)
                    tracking = track_event(product, output)
                    learning = learn_from_results(product, tracking)

                    final_results.append({
                        "product_id": product_id,
                        "slot": slot,
                        "score": product.get("score"),
                        "commission": product.get("commission"),
                        "content": fixed_content,
                        "monetized_content": monetized_content,
                        "routing": routing,
                        "landingpage": landingpage,
                        "compliance": compliance,
                        "landingpage_audit": landingpage_audit,
                        "output": output,
                        "tracking": tracking,
                        "learning": learning,
                        "status": "DIRECT_TO_SHOP" if route.get("landingpage_required") is False else "LANDINGPAGE_V4_ACTIVE"
                    })

                except Exception as item_error:
                    final_results.append({
                        "product_id": item.get("product_id") if isinstance(item, dict) else None,
                        "slot": slot,
                        "status": "ITEM_ERROR",
                        "error": str(item_error),
                        "traceback": traceback.format_exc()
                    })

        return {
            "status": "success",
            "mode": "MASTER_ENGINE_V4_ROUTING_ACTIVE",
            "executed": len(final_results),
            "dashboard": dashboard,
            "results": final_results,
            "sample_product": final_results[0] if final_results else None,
            "time": str(datetime.now())
        }

    except Exception as e:
        return {
            "status": "fatal_error",
            "message": str(e),
            "traceback": traceback.format_exc(),
            "mode": "MASTER_ENGINE_V4_ROUTING_FAILED",
            "executed": 0,
            "dashboard": {},
            "results": [],
            "sample_product": None,
            "time": str(datetime.now())
        }
