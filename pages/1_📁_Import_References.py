
import streamlit as st
import pandas as pd
import rispy
import json
from utils.file_utils import save_project_data, load_project_data

st.set_page_config(page_title="Import References")
st.title("📁 Import References")

project_name = st.text_input("🔖 Project Name", value=st.session_state.get("project_name", "default_project"))
st.session_state["project_name"] = project_name

uploaded_file = st.file_uploader("Upload references (.csv or .ris)")
refs = []

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".ris"):
        entries = rispy.load(uploaded_file)
        df = pd.DataFrame(entries)
    else:
        st.error("Unsupported file format.")
        df = None

    if df is not None:
        st.session_state["references"] = df.to_dict(orient="records")
        st.session_state["decisions"] = {}
        st.success("✅ References imported.")
        st.dataframe(df.head())
        save_project_data(project_name, st.session_state["references"], st.session_state["decisions"])
elif st.button("📂 Load Existing Project"):
    refs, decisions = load_project_data(project_name)
    if refs:
        st.session_state["references"] = refs
        st.session_state["decisions"] = decisions
        st.success("✅ Project loaded.")
