import re
import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix

DATA_PATH = Path("data/dreaddit-test.csv")
MODELS_DIR = Path("models")
MODELS_DIR.mkdir(exist_ok=True)

def clean_text(s: str) -> str:
    s = str(s).lower()
    s = re.sub(r"http\S+|www\.\S+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def guess_columns(df: pd.DataFrame):
    # candidate names
    text_candidates = ["text", "sentence", "post", "content", "body"]
    label_candidates = ["label", "stress", "is_stress", "y", "target"]

    text_col = next((c for c in text_candidates if c in df.columns), None)
    label_col = next((c for c in label_candidates if c in df.columns), None)

    # fallback: pick longest average length column as text
    if text_col is None:
        lengths = {c: df[c].astype(str).str.len().mean() for c in df.columns}
        text_col = max(lengths, key=lengths.get)

    # fallback: pick column with only 2 unique values as label
    if label_col is None:
        binary_cols = []
        for c in df.columns:
            uniq = df[c].dropna().unique()
            if len(uniq) == 2:
                binary_cols.append(c)
        label_col = binary_cols[0] if binary_cols else None

    return text_col, label_col

def main():
    df = pd.read_csv(DATA_PATH)
    text_col, label_col = guess_columns(df)

    if label_col is None:
        raise ValueError(
            f"Could not detect label column. Columns are: {list(df.columns)}. "
            "Tell me your column names and I'll fix the script."
        )

    df = df[[text_col, label_col]].dropna()
    df[text_col] = df[text_col].apply(clean_text)

    # normalize labels to 0/1
    y_raw = df[label_col]
    if y_raw.dtype == object:
        # map common strings
        y = y_raw.astype(str).str.lower().map({"0": 0, "1": 1, "false": 0, "true": 1, "no": 0, "yes": 1})
        if y.isna().any():
            # fallback: factorize
            y = pd.factorize(y_raw)[0]
    else:
        y = y_raw.astype(int)

    X_train, X_val, y_train, y_val = train_test_split(
        df[text_col], y, test_size=0.2, random_state=42, stratify=y
    )

    vec = TfidfVectorizer(ngram_range=(1, 2), max_features=50000, min_df=2)
    Xtr = vec.fit_transform(X_train)
    Xva = vec.transform(X_val)

    clf = LinearSVC()
    clf.fit(Xtr, y_train)

    preds = clf.predict(Xva)
    print("=== Stress model report ===")
    print(classification_report(y_val, preds))
    print("Confusion matrix:\n", confusion_matrix(y_val, preds))

    joblib.dump(vec, MODELS_DIR / "stress_vectorizer.joblib")
    joblib.dump(clf, MODELS_DIR / "stress_model.joblib")

    print("Detected columns:", {"text_col": text_col, "label_col": label_col})
    print("Saved stress model to models/")

if __name__ == "__main__":
    main()
