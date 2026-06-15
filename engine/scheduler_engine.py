def get_time_slot(hour):

    if 6 <= hour < 11:
        return "morning"
    elif 11 <= hour < 17:
        return "midday"
    else:
        return "evening"
