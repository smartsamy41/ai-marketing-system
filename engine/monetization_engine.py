import uuid

from datetime import datetime





def generate_affiliate_link(product):

    product = product if isinstance(product, dict) else {}



    source = str(product.get("source") or "").strip().lower()

    product_id = str(product.get("product_id") or "unknown")



    if "amazon" in source:

        return f"https://amazon.de/dp/{product_id}?tag=freebasics-21"



    if "check24" in source:

        return f"https://check24.de/vergleich/{product_id}?tracking=AI_AGENT"



    if "tarifcheck" in source:

        return f"https://tarifcheck.de/{product_id}?partner=165274"



    if "telekom" in source:

        return f"https://telekom.de/{product_id}"



    return f"https://track.ai/{product_id}?ref={uuid.uuid4()}"





def inject_monetization(content, product, assets):

    content = content if isinstance(content, dict) else {}

    product = product if isinstance(product, dict) else {}



    text = content.get("text") or ""

    title = content.get("title") or product.get("name") or product.get("product_id") or "Produkt"

    affiliate_link = generate_affiliate_link(product)



    return {

        "title": title,

        "text": f"{text}\n\n👉 Jetzt vergleichen: {affiliate_link}",

        "affiliate_link": affiliate_link,

        "tracking_id": str(uuid.uuid4()),

        "timestamp": str(datetime.now()),

        "status": "MONETIZED_OK"

    }
