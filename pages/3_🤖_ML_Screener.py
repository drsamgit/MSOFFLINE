
import streamlit as st
import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.file_utils import save_project_data

st.set_page_config(page_title="ML Screener")
st.title("🤖 ML Screener (SGDClassifier)")

refs = st.session_state.get("references", [])
decisions = st.session_state.get("decisions", {})
project_name = st.session_state.get("project_name", "default_project")

if not refs or not decisions:
    st.warning("No references or decisions available.")
    st.stop()

# Prepare data
texts = [ref.get("title", ref.get("TI", "")) + " " + ref.get("abstract", ref.get("AB", "")) for ref in refs]
labels = [1 if decisions.get(f"ref_{i}") == "Include" else 0 if decisions.get(f"ref_{i}") == "Exclude" else -1 for i in range(len(refs))]

# Only use labeled data for training
train_texts = [t for t, l in zip(texts, labels) if l != -1]
train_labels = [l for l in labels if l != -1]

if len(set(train_labels)) < 2:
    st.warning("Not enough labeled data for training. Label both Include and Exclude to proceed.")
    st.stop()

# Train model
vectorizer = TfidfVectorizer(stop_words="english")
X_train = vectorizer.fit_transform(train_texts)
model = SGDClassifier(random_state=42)
model.fit(X_train, train_labels)

# Predict on all
X_all = vectorizer.transform(texts)
preds = model.predict_proba(X_all)[:, 1]

# Show predictions
for i, prob in enumerate(preds):
    key = f"ref_{i}"
    with st.expander(f"{i+1}. {refs[i].get('title', refs[i].get('TI', 'No Title'))}"):
        st.write(refs[i])
        st.markdown(f"**ML Suggestion:** {'✅ Include' if prob > 0.5 else '❌ Exclude'} ({prob:.2f})")
        decision = st.radio("Your Decision", ["Unscreened", "Include", "Exclude"], index=["Unscreened", "Include", "Exclude"].index(decisions.get(key, "Unscreened")), key=key)
        decisions[key] = decision

st.session_state["decisions"] = decisions

if st.button("💾 Save ML Decisions"):
    save_project_data(project_name, refs, decisions)
    st.success("ML-assisted decisions saved.")
