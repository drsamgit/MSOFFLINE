
import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Export Progress")
st.title("📤 Export Screening Decisions")

refs = st.session_state.get("references", [])
decisions = st.session_state.get("decisions", {})
project_name = st.session_state.get("project_name", "default_project")

if not refs or not decisions:
    st.warning("Nothing to export.")
    st.stop()

# Create DataFrame
data = []
for i, ref in enumerate(refs):
    row = ref.copy()
    row["decision"] = decisions.get(f"ref_{i}", "Unscreened")
    data.append(row)

df = pd.DataFrame(data)

# Export CSV
csv_file = f"{project_name}_screened.csv"
df.to_csv(csv_file, index=False)
with open(csv_file, "rb") as f:
    st.download_button("⬇️ Download CSV", f, file_name=csv_file, mime="text/csv")

# Export RIS
try:
    import rispy
    ris_data = []
    for ref in data:
        if "TI" in ref or "title" in ref:
            ris_entry = {
                "TY": "JOUR",
                "TI": ref.get("TI", ref.get("title", "")),
                "AB": ref.get("AB", ref.get("abstract", "")),
                "N1": f"Decision: {ref['decision']}",
                "ER": ""
            }
            ris_data.append(ris_entry)
    ris_file = f"{project_name}_screened.ris"
    with open(ris_file, "w") as f:
        rispy.dump(ris_data, f)
    with open(ris_file, "rb") as f:
        st.download_button("⬇️ Download RIS", f, file_name=ris_file, mime="application/x-research-info-systems")
except Exception as e:
    st.error(f"RIS export failed: {e}")
