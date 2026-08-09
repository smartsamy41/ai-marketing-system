from datetime import datetime, timezone
import uuid

from engine.bigquery_logger import BigQueryLogger


click_log = []
conversion_log = []
event_log = []


# =========================
# BIGQUERY CONNECTION
# =========================

bq_logger = BigQueryLogger(
    "smartcontent2050",
    "smartcontent"
)


def now():

    return datetime.now(
        timezone.utc
    ).isoformat()



def create_id():

    return str(
        uuid.uuid4()
    )



# =========================
# GENERAL EVENT
# =========================

def track_event(
    event_name,
    product_id=None,
    partner=None,
    asset_id=None,
    landingpage_id=None,
    source="direct",
    channel="direct",
    campaign=None,
    value=None,
    currency="EUR"
):

    event = {

        "event_id":
            create_id(),

        "event_name":
            event_name,

        "timestamp":
            now(),

        "product_id":
            product_id,

        "partner":
            partner,

        "asset_id":
            asset_id,

        "landingpage_id":
            landingpage_id,

        "source":
            source,

        "channel":
            channel,

        "campaign":
            campaign,

        "value":
            value,

        "currency":
            currency

    }


    event_log.append(event)


    # BigQuery events

    bq_logger.log_event(
        event_name,
        event
    )


    return event



# =========================
# CLICK
# =========================

def track_click(
    product,
    source="direct",
    partner=None,
    asset_id=None,
    landingpage_id=None,
    channel="web",
    url=None
):

    event = {

        "product_id":
            product,

        "source":
            source,

        "platform":
            channel,

        "partner":
            partner,

        "asset_id":
            asset_id,

        "landingpage_id":
            landingpage_id,

        "url":
            url or ""

    }


    click_log.append(event)


    bq_logger.log_click(
        event
    )


    track_event(
        "affiliate_click",
        product_id=product,
        partner=partner,
        asset_id=asset_id,
        landingpage_id=landingpage_id,
        source=source,
        channel=channel
    )


    return True



# =========================
# CONVERSION
# =========================

def track_conversion(
    product,
    value,
    partner=None,
    source="direct",
    channel="web"
):


    event = {

        "product_id":
            product,

        "source":
            source,

        "platform":
            channel,

        "partner":
            partner,

        "value":
            float(value)

    }


    conversion_log.append(event)


    bq_logger.log_conversion(
        event
    )


    track_event(
        "conversion",
        product_id=product,
        partner=partner,
        source=source,
        channel=channel,
        value=float(value)
    )


    return True



# =========================
# STATS
# =========================

def get_stats():

    revenue=sum(
        x.get("value",0)
        for x in conversion_log
    )


    return {

        "events":
            len(event_log),

        "clicks":
            len(click_log),

        "conversions":
            len(conversion_log),

        "revenue":
            revenue

    }



# =========================
# EXPORT
# =========================

def get_events():

    return event_log
