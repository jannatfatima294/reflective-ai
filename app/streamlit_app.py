import streamlit as st
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
    c1.metric("Emotional state", out["emotional_state"])
    c2.metric("Cognitive load", out["stress_level"])
    c3.metric("Decision conflict", out["conflict_level"])

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
