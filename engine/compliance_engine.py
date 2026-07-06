def check(content):
    forbidden = ["beste", "günstig", "sparen"]
    return [w for w in forbidden if w in str(content).lower()]
