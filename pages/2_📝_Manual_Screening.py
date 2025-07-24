import streamlit as st
from utils.file_utils import save_project_data

st.set_page_config(page_title="Manual Screening")
st.title("📝 Manual Screening")

refs = st.session_state.get("references", [])
decisions = st.session_state.get("decisions", {})
project_name = st.session_state.get("project_name", "default_project")

if not refs:
    st.warning("⚠️ No references loaded. Please import first.")
    st.stop()

# Initialize decisions if not already
if "decisions" not in st.session_state:
    st.session_state["decisions"] = {}

# Display screening interface
for i, ref in enumerate(refs):
    key = f"ref_{i}"
    title = ref.get("title") or ref.get("TI") or "No Title"
    abstract = ref.get("abstract") or ref.get("AB") or "No Abstract"
    authors = ref.get("authors") or ref.get("AU") or ""
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"**{i+1}. {title}**")
        st.markdown(f"*{authors}*")
        st.markdown(f"`Abstract:` {abstract}")
    with col2:
        selected = st.radio(
            "Decision",
            ["Unscreened", "Include", "Exclude"],
            index=["Unscreened", "Include", "Exclude"].index(decisions.get(key, "Unscreened")),
            key=key,
        )
        st.session_state["decisions"][key] = selected

# Save button
if st.button("💾 Save Screening Decisions"):
    save_project_data(project_name, refs, st.session_state["decisions"])
    st.success("✅ Screening decisions saved.")
