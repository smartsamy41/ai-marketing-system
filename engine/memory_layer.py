import json
import os
from datetime import datetime

# =========================
# 🧠 MEMORY LAYER V1
# =========================

MEMORY_FILE = "/tmp/ai_memory.json"


# -------------------------
# INIT MEMORY STORAGE
# -------------------------
def _load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def _save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)


# -------------------------
# STORE EVENT
# -------------------------
def store_event(event_type, payload):
    memory = _load_memory()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": event_type,
        "payload": payload
    }

    memory.append(entry)
    _save_memory(memory)

    return entry


# -------------------------
# GET MEMORY
# -------------------------
def get_memory(limit=100):
    memory = _load_memory()
    return memory[-limit:]


# -------------------------
# ANALYZE MEMORY
# -------------------------
def analyze_memory():
    memory = _load_memory()

    if not memory:
        return {
            "status": "EMPTY",
            "insight": "No memory data available yet"
        }

    types = {}
    for m in memory:
        t = m["type"]
        types[t] = types.get(t, 0) + 1

    return {
        "status": "ACTIVE_MEMORY",
        "total_events": len(memory),
        "event_distribution": types,
        "last_event": memory[-1]
    }
