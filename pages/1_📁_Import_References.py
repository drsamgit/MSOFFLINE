import streamlit as st
import pandas as pd
import rispy
import json
from utils.file_utils import save_project_data, load_project_data
from io import StringIO

st.set_page_config(page_title="Import References")
st.title("📁 Import References")

# Get project name
project_name = st.text_input("🔖 Project Name", value=st.session_state.get("project_name", "default_project"))
st.session_state["project_name"] = project_name

# Upload reference file
uploaded_file = st.file_uploader("📄 Upload references (.csv or .ris)")
refs = []

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".ris"):
        try:
            ris_text = uploaded_file.read().decode("utf-8")
            entries = rispy.load(StringIO(ris_text))
            df = pd.DataFrame(entries)
        except Exception as e:
            st.error(f"❌ Failed to parse RIS: {e}")
            df = None
    else:
        st.error("❌ Unsupported file format. Please use .csv or .ris")
        df = None

    # Show and save
    if df is not None:
        df = df.fillna("")  # Replace NaNs with empty string
        st.session_state["references"] = df.to_dict(orient="records")
        st.session_state["decisions"] = {}
        st.success("✅ References imported successfully.")
        st.dataframe(df.head())
        save_project_data(project_name, st.session_state["references"], st.session_state["decisions"])

# Load existing project manually
elif st.button("📂 Load Existing Project"):
    refs, decisions = load_project_data(project_name)
    if refs:
        st.session_state["references"] = refs
        st.session_state["decisions"] = decisions
        st.success("✅ Project loaded successfully.")
        st.write(f"Loaded {len(refs)} references.")
    else:
        st.warning("⚠️ No saved project found with this name.")
