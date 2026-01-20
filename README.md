# Reflective AI – Decision Support System

A non-clinical, human-centered AI system that analyzes written text to identify:
- emotional state
- cognitive load (stress)
- decision conflict signals

The system provides reflective insights and prompts to support clarity,
without offering advice or diagnoses.

## Features
- NLP-based emotion classification
- Stress / cognitive load detection
- Explainable decision-conflict cues
- Clean Streamlit interface

## Tech Stack
- Python
- Scikit-learn
- TF-IDF
- Streamlit

## Datasets
- Emotion dataset (Kaggle – Emotions for NLP)
- Stress dataset (Dreaddit / Kaggle)

Datasets are not included in this repository due to licensing.

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
