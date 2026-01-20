import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path (Streamlit Cloud fix)
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.predict import analyze

st.set_page_config(page_title="Reflective AI", page_icon="🧠", layout="centered")

# Simple UI polish (CSS)
st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 900px; }
    h1 { font-size: 2.2rem !important; }

    .big-pill {
      padding: 14px 14px;
      border-radius: 14px;
      border: 1px solid rgba(255,255,255,0.10);
      background: rgba(255,255,255,0.03);
      font-size: 1.05rem;
      font-weight: 600;
      line-height: 1.2;
      word-break: break-word;
    }

    div[data-testid="stAlert"] { border-radius: 14px; }

    .stButton > button {
      border-radius: 14px;
      padding: 0.7rem 1rem;
      font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧠 Reflective AI")
st.caption("Write freely. Get a calm, structured reflection — not advice or diagnosis.")

show_quote = st.toggle("Show soft quote", value=True)

text = st.text_area("Paste your thoughts:", height=180, placeholder="Write freely…")

if st.button("Analyze", use_container_width=True) and text.strip():
    out = analyze(text, show_quote=show_quote)

    st.subheader("Summary")
    st.info(out["summary"])

    c1, c2, c3 = st.columns(3)

    with c1:
        st.caption("Emotional state")
        st.markdown(
            f"<div class='big-pill'>{out['emotional_state']}</div>",
            unsafe_allow_html=True,
        )

    with c2:
        st.caption("Cognitive load")
        st.markdown(
            f"<div class='big-pill'>{out['stress_level']}</div>",
            unsafe_allow_html=True,
        )

    with c3:
        st.caption("Decision conflict")
        st.markdown(
            f"<div class='big-pill'>{out['conflict_level']}</div>",
            unsafe_allow_html=True,
        )

    st.subheader("Reflection prompts")
    for p in out["prompts"]:
        st.write("• " + p)

    if out.get("quote"):
        st.markdown("---")
        st.write("✨ " + out["quote"])

    with st.expander("Signals (for debugging)"):
        st.json(out["explain"])

else:
    st.code(
        "Example:\n"
        "I feel torn between pushing myself and resting. "
        "I'm scared I'll fall behind but I'm exhausted."
    )
