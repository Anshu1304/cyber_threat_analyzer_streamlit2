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
            analysis_result = gpt.analyze_threat(query)  # Analyze the threat
            
            if "error" in analysis_result:
                st.error(analysis_result["error"])
            else:
                st.subheader("📌 AI Analysis Response")
                st.write(analysis_result)

                # Call tag_threat_data to automatically tag the analyzed result
                with st.spinner("Tagging analyzed data..."):
                    tagging_result = gpt.tag_threat_data(analysis_result)  # Tag the result from analysis
                
                    if "error" in tagging_result:
                        st.error(tagging_result["error"])
                    else:
                        st.subheader("🏷️ Tagged Result")
                        st.json(tagging_result)

elif option == "🏷️ Tag Threat Data":
    st.header("🏷️ Threat Tagger")
    data = st.text_area("Enter raw threat data to tag:")

    if st.button("Tag"):
        with st.spinner("Tagging data using AI..."):
            tagging_result = gpt.tag_threat_data(data)
            
            if "error" in tagging_result:
                st.error(tagging_result["error"])
            else:
                st.subheader("🏷️ Tagged Result")
                st.json(tagging_result)

st.markdown("---")
