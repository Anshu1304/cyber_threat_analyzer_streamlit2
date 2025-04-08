import streamlit as st
from gpt_helper2 import GPTHelper
from database import ThreatDatabase

st.set_page_config(page_title="Cyber Threat Analyzer", layout="wide")
st.title("🛡️ Cyber Threat Analyzer")
st.markdown("Analyze and tag cyber threats using AI (Gemma model via OpenRouter)")

gpt = GPTHelper()
db = ThreatDatabase()

option = st.sidebar.radio("Select an action:", ["🔍 Analyze Threat", "🏷️ Tag Threat Data"])

if option == "🔍 Analyze Threat":
    st.header("🔍 Threat Analysis")
    query = st.text_area("Enter threat description to analyze:")
    if st.button("Analyze"):
        with st.spinner("Analyzing threat data using AI..."):
            result = gpt.analyze_threat(query)
            st.subheader("📌 AI Response")
            if result.get("status") == "success":
                content = result["data"].get("content", "No detailed response returned.")
                st.write(content)
                db.save_threat(query, content)
            else:
                st.error(result.get("error", "Unknown error occurred."))

elif option == "🏷️ Tag Threat Data":
    st.header("🏷️ Threat Tagger")
    data = st.text_area("Enter raw threat data to tag:")
    if st.button("Tag"):
        with st.spinner("Tagging data using AI..."):
            result = gpt.tag_threat_data(data)
            st.subheader("📌 Tagged Result")
            if result.get("status") == "success":
                st.json(result["data"])
                db.save_threat(data, str(result["data"]))
            else:
                st.error(result.get("error", "Tagging failed."))

st.markdown("---")
if st.checkbox("📂 Show Saved Threat History"):
    records = db.get_all_threats()
    for record in records:
        st.markdown(f"**🕒 {record[3]}**")
        st.markdown(f"🔎 **Query**: {record[1]}")
        st.markdown(f"📌 **Response**: {record[2]}")
        st.markdown("---")
