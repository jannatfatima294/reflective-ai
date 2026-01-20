import re
import joblib
from pathlib import Path
from src.cues import cue_summary
from src.insights import build_output

MODELS_DIR = Path("models")

def clean_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r"http\S+|www\.\S+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# Load saved artifacts
emotion_vec = joblib.load(MODELS_DIR / "emotion_vectorizer.joblib")
emotion_model = joblib.load(MODELS_DIR / "emotion_model.joblib")
stress_vec = joblib.load(MODELS_DIR / "stress_vectorizer.joblib")
stress_model = joblib.load(MODELS_DIR / "stress_model.joblib")

def stress_to_level(pred: int) -> str:
    # simple mapping (you can refine later)
    return "High" if int(pred) == 1 else "Low"

def analyze(text: str, show_quote: bool = True) -> dict:
    raw = text
    t = clean_text(text)

    # emotion state
    Xe = emotion_vec.transform([t])
    emotional_state = emotion_model.predict(Xe)[0]

    # stress
    Xs = stress_vec.transform([t])
    stress_pred = stress_model.predict(Xs)[0]
    stress_level = stress_to_level(stress_pred)

    cues = cue_summary(raw)
    conflict = cues["conflict"]

    summary, prompts, quote = build_output(emotional_state, stress_level, conflict, show_quote)

    return {
        "emotional_state": emotional_state,
        "stress_level": stress_level,
        "conflict_level": conflict,
        "summary": summary,
        "prompts": prompts,
        "quote": quote,
        "explain": cues,
    }
