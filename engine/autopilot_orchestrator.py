from engine.cycle_manager import CycleManager
from engine.cycle_logger import CycleLogger
from engine.learning_reader import LearningReader
from engine.landingpage_validator import LandingpageValidator

from datetime import datetime, timezone
from google.cloud import bigquery


class AutopilotOrchestrator:

    def __init__(
        self,
        ai,
        content,
        sheets,
        yt,
        pin,
        revenue,
        affiliate=None,
        compliance=None,
        winner_engine=None,
        landingpage_source=None,
        content_storage=None
    ):

        self.ai = ai
        self.content = content
        self.sheets = sheets
        self.youtube = yt
        self.pinterest = pin
        self.revenue = revenue
        self.affiliate = affiliate
        self.compliance = compliance

        self.cycle_manager = CycleManager()
        self.cycle_logger = CycleLogger()
        self.learning_reader = LearningReader()

        self.winner_engine = winner_engine
        self.landingpage_source = landingpage_source
        self.content_storage = content_storage
        self.landingpage_validator = LandingpageValidator()


    def log_post(
        self,
        product_id: str,
        platform: str = "blog",
        post_url: str = "",
        status: str = "generated"
    ):

        client = bigquery.Client(
            project="smartcontent2050"
        )

        table = (
            "smartcontent2050."
            "smartcontent."
            "posts"
        )

        row = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "product_id": product_id,

            "platform": platform,

            "post_url": post_url,

            "status": status
        }

        errors = client.insert_rows_json(
            table,
            [row]
        )

        return {
            "errors": errors,
            "row": row
        }


    def run(self):

        decision = self.ai.decide_next_action()

        if decision.get("action") == "WAIT":

            return {
                "status": "WAIT",
                "reason": decision.get("reason")
            }


        product = decision.get("product")

        if not product:

            return {
                "status": "BLOCKED",
                "reason": "MISSING_PRODUCT"
            }


        if isinstance(product, dict):

            product_id = (
                product.get("product_id")
                or product.get("id")
                or "UNKNOWN_PRODUCT"
            )

        else:

            product_id = str(product)


        cycle = self.cycle_manager.create_run(
            product_id=product_id,
            platform="CONTENT",
            cycle_id="ROUND_1"
        )


        if cycle.get("status") == "BLOCKED":

            return cycle


        self.cycle_logger.log_run(
            run_id=cycle["run_id"],
            cycle_id=cycle["cycle_id"],
            product_id=cycle["product_id"],
            platform=cycle["platform"],
            status="PROCESSING",
            note="Autopilot cycle started"
        )


        generated_content = self.content.generate(
            product
        )


        post_logging_result = self.log_post(
            product_id=product_id,
            platform="blog",
            status="generated"
        )


        blog_storage_result = {
            "status": "SKIPPED",
            "reason": "NO_STORAGE"
        }


        if self.content_storage:

            try:

                blog_storage_result = self.content_storage.append(
                    "blog_posts",
                    [
                        product_id,
                        generated_content.get("title", ""),
                        generated_content.get("seo_title", ""),
                        generated_content.get("description", ""),
                        generated_content.get("body", ""),
                        str(generated_content.get("faq", "")),
                        "generated"
                    ]
                )

            except Exception as error:

                blog_storage_result = {
                    "status": "ERROR",
                    "error": str(error)
                }


        landingpage_validation = {
            "status": "NOT_CONFIGURED",
            "product_id": product_id,
            "errors": [],
            "warnings": []
        }


        if self.landingpage_source:

            landingpage_records = (
                self.landingpage_source.read_records(
                    "landingpages",
                    "A:ZZ"
                )
            )

            landingpage_record = next(
                (
                    record
                    for record in landingpage_records
                    if str(
                        record.get("product_id") or ""
                    ).strip().lower()
                    == str(product_id).strip().lower()
                ),
                None
            )

            if landingpage_record:

                landingpage_validation = (
                    self.landingpage_validator.validate(
                        landingpage_record,
                        partner=landingpage_record.get(
                            "partner"
                        )
                    )
                )

            else:

                landingpage_validation = {
                    "status": "NOT_FOUND",
                    "product_id": product_id,
                    "errors": [],
                    "warnings": [
                        "Landingpage record not found"
                    ]
                }


        if landingpage_validation.get(
            "status"
        ) == "BLOCKED":

            self.cycle_logger.log_run(
                run_id=cycle["run_id"],
                cycle_id=cycle["cycle_id"],
                product_id=cycle["product_id"],
                platform=cycle["platform"],
                status="BLOCKED",
                note=(
                    "MLP005 Landingpage validation failed | "
                    f"status={landingpage_validation.get('status')} | "
                    f"errors={landingpage_validation.get('errors')}"
                )
            )


            return {
                "status": "BLOCKED",
                "reason": "LANDINGPAGE_VALIDATION_FAILED",
                "landingpage_validation": landingpage_validation
            }


        compliance_result = {
            "status": "NOT_CONFIGURED",
            "errors": [],
            "partner_rules": []
        }


        partner = None


        if self.affiliate:

            initial_product_data = self.affiliate.get_product_data(
                product
            )

            if initial_product_data.get("status") == "FOUND":

                partner = initial_product_data.get(
                    "source"
                )


        if self.compliance:

            compliance_result = self.compliance.audit(
                generated_content,
                partner=partner
            )


            if compliance_result.get("status") == "BLOCKED":

                self.cycle_logger.log_run(
                    run_id=cycle["run_id"],
                    cycle_id=cycle["cycle_id"],
                    product_id=cycle["product_id"],
                    platform=cycle["platform"],
                    status="BLOCKED",
                    note="Compliance failed"
                )


                return {
                    "status": "BLOCKED",
                    "reason": "COMPLIANCE_FAILED",
                    "audit": compliance_result
                }


        winner_result = {

            "winner_status": False,
            "video_allowed": False,
            "voice_allowed": False,
            "reason": "NO_WINNER_ENGINE"

        }


        if self.winner_engine:

            learning_data = (
                self.learning_reader.get_product_learning(
                    product_id
                )
            )


            if learning_data:

                money_score = float(
                    learning_data.get(
                        "money_score",
                        0
                    ) or 0
                )

                ctr = float(
                    learning_data.get(
                        "ctr",
                        0
                    ) or 0
                )

                conversions = int(
                    learning_data.get(
                        "conversions",
                        0
                    ) or 0
                )

                earnings = float(
                    learning_data.get(
                        "earnings",
                        0
                    ) or 0
                )


            else:

                money_score = 0
                ctr = 0
                conversions = 0
                earnings = 0


            winner_result = self.winner_engine.evaluate(

                money_score=money_score,

                ctr=ctr,

                conversions=conversions,

                earnings=earnings,

                compliance_status=
                    compliance_result.get(
                        "status",
                        "OK"
                    )

            )


        affiliate_link = None
        tracking_link = None
        landingpage_link = None
        product_data = None


        if self.affiliate:

            product_data = self.affiliate.get_product_data(
                product
            )


            if product_data.get("status") == "FOUND":

                affiliate_link = product_data.get(
                    "affiliate_url"
                )

                tracking_link = product_data.get(
                    "tracking_url"
                )

                landingpage_link = product_data.get(
                    "landingpage_url"
                )


        youtube_result = {

            "status":
                "WINNER_APPROVED"
                if winner_result.get(
                    "video_allowed"
                )
                else "NOT_ALLOWED",

            "voice_allowed":
                winner_result.get(
                    "voice_allowed"
                ),

            "reason":
                winner_result.get(
                    "reason"
                )

        }


        pinterest_result = {

            "status":
                "waiting_for_image_asset",

            "target_url":
                landingpage_link

        }


        self.cycle_logger.update_status(
            run_id=cycle["run_id"],
            cycle_id=cycle["cycle_id"],
            product_id=cycle["product_id"],
            platform=cycle["platform"],
            status="ROUND_1_COMPLETE",
            note="Production content cycle completed"
        )


        return {

            "status": "READY",

            "run_id": cycle["run_id"],

            "cycle_id": cycle["cycle_id"],

            "product_id": cycle["product_id"],

            "product": product,

            "content": generated_content,

            "partner": partner,

            "affiliate_link": affiliate_link,

            "tracking_link": tracking_link,

            "landingpage_link": landingpage_link,

            "product_data": product_data,

            "landingpage_validation": landingpage_validation,

            "compliance": compliance_result,

            "winner": winner_result,

            "youtube": youtube_result,

            "pinterest": pinterest_result,

            "revenue": self.revenue.stats()

        }
