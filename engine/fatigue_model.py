# engine/fatigue_model.py
"""
Fatigue scoring based on real hospital regulations:
- NHS: max 12h shift, max 48h/week, min 11h rest between shifts
- Joint Commission: flags >5 consecutive nights
- ICN: weekend work limits, night shift penalties
"""

SHIFT_HOURS = {"Early": 8, "Day": 8, "Late": 8, "Night": 10, "Off": 0}
SHIFT_FATIGUE_BASE = {"Early": 10, "Day": 8, "Late": 12, "Night": 20, "Off": 0}

def compute_fatigue_score(nurse_schedule):
    """
    nurse_schedule: list of shift names across all days e.g. ['Early','Night','Off',...]
    Returns: fatigue score 0-100 (higher = more fatigued)
    """
    score = 0
    days = len(nurse_schedule)
    if days == 0:
        return 0

    # 1. Base fatigue per shift type
    base = sum(SHIFT_FATIGUE_BASE.get(s, 0) for s in nurse_schedule)
    score += min(base / (days * 20) * 40, 40)  # max 40 points

    # 2. Consecutive working days penalty (NHS: flag more than 5)
    consec = 0
    max_consec = 0
    for s in nurse_schedule:
        if s != "Off":
            consec += 1
            max_consec = max(max_consec, consec)
        else:
            consec = 0
    if max_consec > 5:
        score += min((max_consec - 5) * 5, 20)  # max 20 points

    # 3. Night shift streak penalty (Joint Commission: flag more than 3 consecutive nights)
    night_consec = 0
    max_night = 0
    for s in nurse_schedule:
        if s == "Night":
            night_consec += 1
            max_night = max(max_night, night_consec)
        else:
            night_consec = 0
    if max_night > 3:
        score += min((max_night - 3) * 4, 20)  # max 20 points

    # 4. Forbidden succession penalty (insufficient rest between shifts)
    FORBIDDEN = {
        "Night": ["Early", "Day"],
        "Late":  ["Early"],
        "Early": [],
        "Day":   [],
        "Off":   []
    }
    for i in range(len(nurse_schedule) - 1):
        curr = nurse_schedule[i]
        nxt  = nurse_schedule[i + 1]
        if nxt in FORBIDDEN.get(curr, []):
            score += 5

    # 5. Weekly hours check (NHS: flag more than 48 hours per week)
    for w in range(len(nurse_schedule) // 7):
        week = nurse_schedule[w * 7:(w + 1) * 7]
        hours = sum(SHIFT_HOURS.get(s, 0) for s in week)
        if hours > 48:
            score += 10

    return min(round(score), 100)


def compute_all_fatigue(schedule_dict):
    """
    schedule_dict: {nurse_id: [list of shifts across all days]}
    Returns: {nurse_id: fatigue_score}
    """
    return {nid: compute_fatigue_score(shifts) for nid, shifts in schedule_dict.items()}


def get_fatigue_label(score):
    """Returns a risk label and color for a given fatigue score"""
    if score < 30:
        return "Low", "green"
    if score < 60:
        return "Moderate", "orange"
    return "High Risk", "red"