clicks = []
conversions = []

def track_click(product):
    clicks.append(product)
    return {"status": "ok"}

def track_conversion(value):
    conversions.append(value)
    return {"status": "ok"}
