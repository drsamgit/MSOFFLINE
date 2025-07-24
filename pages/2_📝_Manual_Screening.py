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

for i, ref in enumerate(refs):
    key = f"ref_{i}"
    title = ref.get("title") or ref.get("TI") or "No Title"
    with st.expander(f"{i+1}. {title}"):
        st.write(ref)
        current_decision = st.session_state["decisions"].get(key, "Unscreened")
        new_decision = st.radio(
            "Screening Decision",
            ["Unscreened", "Include", "Exclude"],
            index=["Unscreened", "Include", "Exclude"].index(current_decision),
            key=key,
        )
        st.session_state["decisions"][key] = new_decision

if st.button("💾 Save Manual Decisions"):
    st.session_state["decisions"] = dict(st.session_state["decisions"])  # sync session
    save_project_data(project_name, refs, st.session_state["decisions"])
    st.success("✅ Manual decisions saved.")
