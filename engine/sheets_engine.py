from datetime import datetime

DATA = {
    "clicks": [],
    "conversions": [],
    "products": []
}

def log_click(product):
    DATA["clicks"].append({
        "product": product,
        "time": datetime.utcnow().isoformat()
    })

def log_conversion(product, value):
    DATA["conversions"].append({
        "product": product,
        "value": value,
        "time": datetime.utcnow().isoformat()
    })

def get_learning_data():
    return DATA
