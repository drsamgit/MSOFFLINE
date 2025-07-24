
import streamlit as st
from utils.file_utils import save_project_data

st.set_page_config(page_title="Manual Screening")
st.title("📝 Manual Screening")

refs = st.session_state.get("references", [])
decisions = st.session_state.get("decisions", {})
project_name = st.session_state.get("project_name", "default_project")

if not refs:
    st.warning("No references loaded.")
    st.stop()

for i, ref in enumerate(refs):
    key = f"ref_{i}"
    with st.expander(f"{i+1}. {ref.get('title', ref.get('TI', 'No Title'))}"):
        st.write(ref)
        decision = st.radio("Decision", ["Unscreened", "Include", "Exclude"], index=["Unscreened", "Include", "Exclude"].index(decisions.get(key, "Unscreened")), key=key)
        decisions[key] = decision

st.session_state["decisions"] = decisions

if st.button("💾 Save Progress"):
    save_project_data(project_name, refs, decisions)
    st.success("Progress saved.")
