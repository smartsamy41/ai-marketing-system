def update_score(score, clicks, sales):

    if sales > 0:
        score += 10

    if clicks > 50 and sales == 0:
        score -= 5

    return max(0, min(100, score))
