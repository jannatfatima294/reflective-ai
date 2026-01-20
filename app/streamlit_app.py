import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path (Streamlit Cloud fix)
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.predict import analyze


st.set_page_config(page_title="Reflective AI", page_icon="🧠", layout="centered")

st.title("🧠 Reflective AI")
st.caption("Non-clinical reflection & decision-support based on text signals.")

show_quote = st.toggle("Show soft quote", value=True)

text = st.text_area("Paste your thoughts:", height=180, placeholder="Write freely…")

if st.button("Analyze", use_container_width=True) and text.strip():
    out = analyze(text, show_quote=show_quote)

    st.subheader("Summary")
    st.info(out["summary"])

    c1, c2, c3 = st.columns(3)

with c1:
    st.caption("Emotional state")
    st.markdown(f"<div class='big-pill'>{out['emotional_state']}</div>", unsafe_allow_html=True)

with c2:
    st.caption("Cognitive load")
    st.markdown(f"<div class='big-pill'>{out['stress_level']}</div>", unsafe_allow_html=True)

with c3:
    st.caption("Decision conflict")
    st.markdown(f"<div class='big-pill'>{out['conflict_level']}</div>", unsafe_allow_html=True)


    st.subheader("Reflection prompts")
    for p in out["prompts"]:
        st.write("• " + p)

    if out["quote"]:
        st.markdown("---")
        st.write("✨ " + out["quote"])

    with st.expander("Signals (for debugging)"):
        st.json(out["explain"])
else:
    st.code("Example:\nI feel torn between pushing myself and resting. I'm scared I'll fall behind but I'm exhausted.")


