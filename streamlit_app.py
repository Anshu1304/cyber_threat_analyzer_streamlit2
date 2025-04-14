import streamlit as st
from gpt_helper2 import GPTHelper
from database import ThreatDatabase
import datetime

st.set_page_config(page_title="Cyber Threat Analyzer", layout="wide")
st.title("🛡️ Cyber Threat Analyzer")
st.markdown("Analyze and tag cyber threats using AI (Gemma model via OpenRouter)")

gpt = GPTHelper()
db = ThreatDatabase()

option = st.sidebar.radio(
    "Select an action:",
    ["🔍 Analyze Threat", "🏷️ Tag Threat Data"]
)

if option == "🔍 Analyze Threat":
    st.header("🔍 Threat Analysis")
    query = st.text_area("Enter threat description to analyze:")
    if st.button("Analyze"):
        with st.spinner("Analyzing threat data using AI..."):
            result = gpt.analyze_threat(query)
            st.subheader("📌 AI Response")
            if result:
                st.write(result)
                db.save_threat(query, result)
            else:
                st.error("No response received from AI.")

elif option == "🏷️ Tag Threat Data":
    st.header("🏷️ Threat Tagger")
    data = st.text_area("Enter raw threat data to tag:")
    if st.button("Tag"):
        with st.spinner("Tagging data using AI..."):
            result = gpt.tag_threat_data(data)
            st.subheader("📌 Tagged Result")
            if result:
                st.write(result)
                db.save_threat(data, result)
            else:
                st.error("No response received from AI.")

st.markdown("---")

if st.checkbox("📂 Show Saved Threat History"):
    records = db.get_all_threats()
    if records:
        for record in records:
            st.markdown(f"**🕒 {record[3]}**")
            st.markdown(f"🔎 **Query**: {record[1]}")
            st.markdown(f"📌 **Response**: {record[2]}")
            st.markdown("---")
    else:
        st.write("No saved threat history available.")
