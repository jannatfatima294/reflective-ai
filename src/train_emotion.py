import re
import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

DATA_PATH = Path("data/train.txt")
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

def clean_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r"http\S+|www\.\S+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def load_emotion_txt(path: Path) -> pd.DataFrame:
    texts, labels = [], []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # format: text;label
            if ";" not in line:
                continue
            text, label = line.rsplit(";", 1)
            text = text.strip()
            label = label.strip()
            if text and label:
                texts.append(clean_text(text))
                labels.append(label)
    df = pd.DataFrame({"text": texts, "label": labels})
    return df

def map_to_states(raw_label: str) -> str:
    # Your 5 states
    # Calm/Stable is inferred elsewhere; dataset has no neutral label.
    mapping = {
        "joy": "Positive / Hopeful",
        "love": "Positive / Hopeful",
        "sadness": "Heavy / Low",
        "fear": "Anxious / Tense",
        "anger": "Anxious / Tense",
        "surprise": "Conflicted / Uncertain",
    }
    return mapping.get(raw_label, "Conflicted / Uncertain")

def main():
    df = load_emotion_txt(DATA_PATH)
    df["state"] = df["label"].apply(map_to_states)

    X_train, X_val, y_train, y_val = train_test_split(
        df["text"], df["state"], test_size=0.2, random_state=42, stratify=df["state"]
    )

    vec = TfidfVectorizer(ngram_range=(1, 2), max_features=60000, min_df=2)
    Xtr = vec.fit_transform(X_train)
    Xva = vec.transform(X_val)

    clf = LogisticRegression(max_iter=2000, n_jobs=-1)
    clf.fit(Xtr, y_train)

    preds = clf.predict(Xva)
    print("=== Emotion (State) model report ===")
    print(classification_report(y_val, preds))
    print("Confusion matrix:\n", confusion_matrix(y_val, preds))

    joblib.dump(vec, MODELS_DIR / "emotion_vectorizer.joblib")
    joblib.dump(clf, MODELS_DIR / "emotion_model.joblib")

    print("Saved emotion model to models/")

if __name__ == "__main__":
    main()
