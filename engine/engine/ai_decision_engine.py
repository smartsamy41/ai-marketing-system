def choose_best(products):

    best = None
    best_score = 0

    for p in products:
        if p["score"] > best_score:
            best = p
            best_score = p["score"]

    return best
