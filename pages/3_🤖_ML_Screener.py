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
    st.warning("⚠️ No references or decisions available.")
    st.stop()

# Fallback-safe extractor
def get_field(ref, keys, default=""):
    for key in keys:
        value = ref.get(key)
        if value and isinstance(value, str) and value.strip():
            return value.strip()
    return default

# Combine text for vectorizer
texts = [
    f"{get_field(ref, ['title', 'Title', 'TI', 'ArticleTitle'])} {get_field(ref, ['abstract', 'Abstract', 'AB'])}"
    for ref in refs
]
labels = [
    1 if decisions.get(f"ref_{i}") == "Include"
    else 0 if decisions.get(f"ref_{i}") == "Exclude"
    else -1
    for i in range(len(refs))
]

# Filter training data
train_data = [(t, l) for t, l in zip(texts, labels) if l != -1 and t.strip()]
if not train_data:
    st.warning("⚠️ No usable training data. Label at least one Include and one Exclude with valid text.")
    st.stop()

train_texts, train_labels = zip(*train_data)

# Train model
try:
    vectorizer = TfidfVectorizer(stop_words="english")
    X_train = vectorizer.fit_transform(train_texts)

    model = SGDClassifier(loss="log_loss", random_state=42)
    model.fit(X_train, train_labels)

    X_all = vectorizer.transform(texts)
    preds = model.predict_proba(X_all)[:, 1]
except Exception as e:
    st.error(f"❌ ML training failed: {e}")
    st.stop()

# Display predictions and manual decision override
for i, prob in enumerate(preds):
    key = f"ref_{i}"
    ref = refs[i]
    title = get_field(ref, ["title", "Title", "TI", "ArticleTitle"], "No Title")
    abstract = get_field(ref, ["abstract", "Abstract", "AB"], "")
    authors = get_field(ref, ["authors", "AU", "Author"], "")

    with st.expander(f"{i+1}. {title}"):
        if authors:
            st.markdown(f"*{authors}*")
        st.markdown(f"`Abstract:` {abstract}")
        st.markdown(f"**🤖 ML Suggestion:** {'✅ Include' if prob > 0.5 else '❌ Exclude'} (confidence: `{prob:.2f}`)")
        decision = st.radio(
            "Your Decision",
            ["Unscreened", "Include", "Exclude"],
            index=["Unscreened", "Include", "Exclude"].index(decisions.get(key, "Unscreened")),
            key=key,
        )
        decisions[key] = decision

st.session_state["decisions"] = decisions

if st.button("💾 Save ML Decisions"):
    save_project_data(project_name, refs, decisions)
    st.success("✅ ML-assisted decisions saved.")
