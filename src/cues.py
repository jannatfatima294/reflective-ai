CONFLICT = ["but", "however", "although", "yet", "on the other hand"]
UNCERTAINTY = ["maybe", "not sure", "confused", "idk", "i don't know", "uncertain"]
PRESSURE = ["must", "have to", "should", "need to", "can't", "cannot"]
FEAR = ["afraid", "scared", "what if", "worry", "worried", "anxious"]

def _hits(t: str, words) -> int:
    t = t.lower()
    return sum(1 for w in words if w in t)

def conflict_level(text: str) -> str:
    h = _hits(text, CONFLICT) + _hits(text, UNCERTAINTY)
    if h >= 4: return "High"
    if h >= 2: return "Medium"
    if h >= 1: return "Low"
    return "Low"

def cue_summary(text: str) -> dict:
    return {
        "conflict": conflict_level(text),
        "uncertainty_hits": _hits(text, UNCERTAINTY),
        "pressure_hits": _hits(text, PRESSURE),
        "fear_hits": _hits(text, FEAR),
        "conflict_hits": _hits(text, CONFLICT),
    }
